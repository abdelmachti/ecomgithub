from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
from .models import  BillingProfile, Card

# Create your views here.

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_ieC1NVzyI7aQLqhlk4qFd3pA001kPqBlMt" )
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY ","pk_test_v4ND5Ox2C9Aypc9iIfYtc8HS00Je7Wv8AI")
stripe.api_key = STRIPE_SECRET_KEY

def payment_method_view(request):
    """ if request.method == "POST":
        print(request.POST) """
    billing_profile, billing_profile_created= BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart")
    next_url = None
    next_=request.GET.get('next')
    if is_safe_url(next_,request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html',{"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_createview(request):
    if request.method=='POST' and request.is_ajax():
        billing_profile , billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message":"Cannot find this user"}, status_code=401)
        token = request.POST.get("token")
        #print(request.POST) to see with parameter is called #token
        if token is not None:
            """ customer = stripe.Customer.retrieve(billing_profile.customer_id)
            card_response = customer.sources.create(source=token)
            card_obj = Card.objects.add_new(billing_profile, card_response) """
            card_obj = Card.objects.add_new(billing_profile, token)
            print("cart views billing",card_obj)
        return JsonResponse ({"message":"Done!! Your card is already added"})
    return HttpResponse("error", status_code=401)


