from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product
from carts.models import Cart
#from analytics.signals import object_viewed_signal
from analytics.mixins import ObejctViewedMixin
# Create your views here.

class ProductFeaturedListView(ListView):
    template_name="products/list.html"

    def get_queryset(self, *args, **kwargs):
        #request = self.request
        return Product.objects.all().featured()

class ProductFeaturedDetailView(ObejctViewedMixin, DetailView):
    queryset = Product.objects.all().featured()
    template_name="products/featuredDetail.html"

    # get_object()
    """ def get_queryset(self, *args, **kwargs):
        #request = self.request
        return Product.objects.all().featured() """



class ProductListView(ListView):
    #queryset = Product.objects.all()
    template_name= "products/list.html"

    """*def get_context_data(self, *args, **kwargs):
        context= super(ProductListView, self).get_context_data(*args, **kwargs)
        print (context)
        return context"""
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj= Cart.objects.new_or_get(self.request)
        context['cart']= cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()

def Product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list':queryset
    }
    return render(request,"products/list.html",context)

class ProductDetailSlugView(ObejctViewedMixin, DetailView):
    queryset=Product.objects.all()
    template_name="products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj= Cart.objects.new_or_get(self.request)
        context['cart']= cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request= self.request
        slug =self.kwargs.get('slug')
        
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404 ("No Product with this slug")
        except Product.MultipleObjectsReturned:
            qs= Product.objects.filter(slug=slug, active=True)
            if qs.count() != 1:
                instance = qs.first()
        except:
            raise Http404("Ualala")
        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return instance

class ProductDetailView(ObejctViewedMixin, DetailView):
    #queryset = Product.objects.all()
    template_name= "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context= super(ProductDetailView, self).get_context_data(*args, **kwargs)
        #print (context)
        return context
    
    def get_object(self, *args, **kwargs):
        #request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("the product in list is not available")
        return instance

    """ def get_queryset(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        return Product.objects.filter(pk=pk) """


def Product_detail_view(request,pk=None,*args,**kwargs):
    #print(args)
    #print(kwargs)
    #instance= Product.objects.get(pk=pk)
    #instance = get_object_or_404(Product,pk=pk)

    """try:
        instance= Product.objects.get(id=pk)
    except Product.DoesNotExist:
        print("Product is not available")
        raise Http404('Product is not here')
    except:
        print("heeho")"""
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("the Product is not available")

    """qs= Product.objects.filter(id=pk)
    if qs.exists() and qs.count()==1:
        instance=qs.first()
    else:
        raise Http404("Product fuck off")"""



    context = {
        'object':instance
    }
    return render(request,"products/detail.html",context)