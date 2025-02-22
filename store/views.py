from django.template import loader
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from .models import Product, Cart, Category
from django.contrib. auth.models import User
from django.core.exceptions import ObjectDoesNotExist

import stripe
import environ

env = environ.Env()
environ.Env.read_env()


stripe.api_key = env('STRIPE_API_KEY')

YOUR_DOMAIN = 'http://127.0.0.1:8000'

def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    all_categories = Category.objects.all()
    product_json = serializers.serialize('json', Product.objects.filter(pk=product_id))

    template = loader.get_template('store/product.html')

    context = {
       'product_id': product_id,
       'product': product,
       'product_json': product_json,
       'categories': all_categories
       
    }
    return HttpResponse(template.render(context, request))

def login_page(request):

    context = {}

    template = loader.get_template('store/login.html')
    return HttpResponse(template.render(context, request))

def cancel_payment(request):

    context = {}

    template = loader.get_template('store/cancel.html')
    return HttpResponse(template.render(context, request))

def create_user(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    user = User.objects.create_user(username=username,email=email, password=password)
    logUser = authenticate(request, username=username, password=password)

    if logUser is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/login_page')
    

def register_page(request):
   
    context = {}

    template = loader.get_template('store/register.html')
    return HttpResponse(template.render(context, request))

def authentication(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
   
    if user is not None:
        login(request, user)
        return redirect('/')
        
    else:
        return redirect('/login_page')


def addProduct(request):

    productId = request.GET['id']
    product = Product.objects.get(pk=productId)
    user = None
    try:
        user = User.objects.get(pk=request.user.id)
        try:
            cart = Cart.objects.get(owner=request.user.id)
            cart.products.add(product)
            cart.save()
            return redirect('/cart')

        except ObjectDoesNotExist:
            cart = Cart(owner=user, totalPrice=0)
            cart.save()
            cart.products.add(product)
            cart.save()
            return redirect('/cart')
    except ObjectDoesNotExist:
        return redirect('login_page')
        
   
def removeProduct(request):

    productId = request.GET['id']
    product = Product.objects.get(pk=productId)

    cart = Cart.objects.get(owner=request.user.id)
    cart.products.remove(product)
    cart.save()

    return redirect('/cart')

def cart(request):
    cart = Cart.objects.get(owner=request.user.id)
    products = cart.products.all()
    
    context = {
        'cart': cart,
        'products': products
    }
    template = loader.get_template('store/cart.html')
    empty_template = loader.get_template('store/empty_cart.html')

    if products:
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse(empty_template.render(context, request))

def checkout(request):
    cart = Cart.objects.get(owner=request.user.id)
    products = cart.products.all()
    
    context = {
        'cart': cart,
        'products': products
    }
    template = loader.get_template('store/checkout.html')

    if products:
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')



def create(request):
    cart = Cart.objects.get(owner=request.user.id)

    try:

        product = stripe.Product.create(
        name='order',
        )
        
        price = stripe.Price.create(
        product=product.id,
        unit_amount=(int(cart.total_price() * 100)),
        currency='usd',
        )

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # TODO: replace this with the `price` of the product you want to sell
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            payment_method_types=[
              'card'
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
    except Exception as e:
        print(e)
    
    return redirect(checkout_session.url, code=303)



def index(request):
    o = 'name'
    order = request.GET.get('order', None)
    if order == 'price_asc':
        o = 'price'

    if order == 'price_desc':
        o = '-price'

    f = {}
    base_category = request.GET.get('base_category', None)
    if(base_category):
        f['categories__name__iexact'] = base_category
    
        
    index_products = Product.objects.filter(**f).order_by(o)
    all_categories = Category.objects.all()

    template = loader.get_template('store/index.html')
    context = {
        'title': '50% OFF prices so cheap',
        'products': index_products,
        'category1': base_category,
        'categories': all_categories
    }
    return HttpResponse(template.render(context, request))
