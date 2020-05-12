#from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product

# Create your views here.

class SearchProductView(ListView):
    template_name="search/view.html"
    

    def get_context_data(self, *args,**kwargs):
        context =super(SearchProductView, self).get_context_data(*args,**kwargs)
        context['query']=self.request.GET.get('q')
        #print(context)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict= request.GET
        # print('Youpi',method_dict)
        query= method_dict.get('q', None)
        #lookups = Q(title__icontains=query)
        if query is not None:
            # print(Product.objects.search(query))
            return Product.objects.search(query)
        return Product.objects.featured()
