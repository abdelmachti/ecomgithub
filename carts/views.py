from django.conf import  settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from orders.models import Order
from .models import Cart
from accounts.forms import LoginForm , GuestForm
from addresses.forms import AddressForm
from addresses.models import Address
from accounts.models import GuestEmail
from products.models import Product
from billing.models import BillingProfile
# Create your views here.

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_ieC1NVzyI7aQLqhlk4qFd3pA001kPqBlMt" )
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY ","pk_test_v4ND5Ox2C9Aypc9iIfYtc8HS00Je7Wv8AI")

def cart_detail_api_view(request):
    cart_obj , new_obj = Cart.objects.new_or_get(request)
    products = [{
            "id":x.id,
            "url": x.get_absolute_url(),
            "name" :x.name ,
            "price": x.price} 
            for x in cart_obj.products.all()]
    """ jsonlist = list
    for x in cart_obj.products.all():
        data = {"name":x.name, "price":x.price}
        jsonlist.append(data) """
    cart_data = {"products": products, "subtotal":cart_obj.subtotal, "total": cart_obj.total}
    return  JsonResponse(cart_data)

def cart_create(user=None):
    cart_obj= Cart.objects.create(user=None)
    return cart_obj

def cart_home(request):
    #request.session['cart_id']="12"
    #cart_id= request.session.get("cart_id", None)
    #print(cart_id)
    #print(request.session.session_key)
    """ cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = cart_obj.products.all()
    total = 0
    for x in products:
        total += x.price
    print(total)
    cart_obj.total = total
    cart_obj.save() """
    """ cart_id= request.session.get("cart_id", None)
    qs= Cart.objects.filter(id=cart_id)
    if  qs.count() == 1:
        print("ID cart exist")
        cart_obj= qs.first()
        if request.user.is_authenticated  and cart_obj.user is None:
            cart_obj.user= request.user
            cart_obj.save()
    else:
        print("Create new cart")
        #cart_obj= cart_create()
        cart_obj = Cart.objects.new_cart(user=request.user)
        request.session['cart_id']=cart_obj.id """
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html",{"cart":cart_obj})

def cart_update(request):
    #print("request",request.POST.get("product_id"))
    product_id= request.POST.get("product_id")
    
    if product_id is not None:
        try:
            product_obj= Product.objects.get(id=product_id)
            #print("OBJEKT",product_obj)
        except Product.DoesNotExist:
            return redirect("cart:home")
        cart_obj, new_obj= Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added= False
        else:
            cart_obj.products.add(product_obj)
            added=True
        request.session['cart_items']=cart_obj.products.count()
        if request.is_ajax():
            #print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data, status= 200) # status = 400 bad request etc 
           # return JsonResponse({"message":"Error 400"}, status = 400)
    else:
        redirect ("cart:home")
    return redirect ("cart:home")

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_profile , billing_profile_created = BillingProfile.objects.new_or_get(request)
    print("cartsviews",billing_profile)
    """ if billing_profile.count() != 1:
        billing_profile """
    shipping_address_id = request.session.get('shipping_address_id', None)
    billing_address_id  = request.session.get('billing_address_id', None)

    
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile= billing_profile)
        order_obj , order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = billing_profile.has_card
    if request.method == 'POST':
        "check that order is done"
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, charge_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                    print("inactive", billing_profile.set_cards_inactive())
                return redirect("cart:success")
            else:
                print(charge_msg)
                return redirect("cart:checkout")
                    
    """ user = request.user
    billing_profile = None
    guest_email_id= request.session.get('guest_email_id')
    #print(guest_email_id)
    if user.is_authenticated:
        'logged in user checkout, rember payment stuff'
        billing_profile , billing_profile_created = BillingProfile.objects.get_or_create(user=user , email=user.email)
    elif guest_email_id is not None:
        'guest user, reloads payment stuff'
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        #print(guest_email_obj.email)
        billing_profile , billing_guest_progile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    else:
        pass """

    #First Process but gives each refreshing new order id
    """  if billing_profile is not None:
        order_qs = Order.objects.filter(cart=cart_obj, active=True)
        if order_qs.exists():
            order_qs.update(active=False)
        else:
            order_obj  = Order.objects.create(  billing_profile=billing_profile,
                                                cart=cart_obj
                                            ) """
    # Second Process more bette but in OrderMAnager would be more cleaner
    """ if billing_profile is not None:
        order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if order_qs.count()==1:
            order_obj=order_qs.first()
        else:
            
            order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj) """




    context = {
        "object"          : order_obj,
        "billing_profile" : billing_profile,
        "login_form"      : login_form,
        "guest_form"      : guest_form,
        "address_form"    : address_form,
        "address_qs"      : address_qs,
        "has_card"        : has_card,
        "publish_key"     : STRIPE_PUB_KEY
    }
    return render(request, "carts/checkout.html", context )

def checkout_done(request):
    return render(request, "carts/checkout_done.html", {})

        
