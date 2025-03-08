from django.template import loader
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, Category, Order
from django.contrib. auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import uuid

import stripe
import environ

env = environ.Env()
environ.Env.read_env()

stripe.api_key = env('STRIPE_API_KEY')

YOUR_DOMAIN = env('STRIPE_REDIRECT_DOMAIN')

def product(request, product_id):
    product = Product.objects.get(publicId=product_id)
    all_categories = Category.objects.all()

    template = loader.get_template('store/product.html')

    context = {
       'product_id': product_id,
       'product': product,
       'categories': all_categories
    }
    return HttpResponse(template.render(context, request))

def login_page(request):
    template = loader.get_template('store/login.html')
    return HttpResponse(template.render({}, request))

def cancel_payment(request):
    template = loader.get_template('store/cancel.html')
    return HttpResponse(template.render(request))

def success_payment(request):
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                orderNumberParam = request.GET.get('orderNumber', None)
                order = Order.objects.get(orderNumber=orderNumberParam)
                products = order.products.all()
               
                if order:
                    order.paymentStatus = "APPROVED"
                    order.save()

                    context = {
                        'order': order,
                        'products': products
                    }

                    template = loader.get_template('store/success.html')
                    return HttpResponse(template.render(context, request))
                else: return redirect('/not-found') 
            else:
                return redirect('/cancel')  
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    else:
        return redirect('/cancel')


def logout_view(request):
    logout(request)
    return redirect('/login_page')

def user(request):
    menu = request.GET.get('menu', None)
    orders = Order.objects.all().filter(owner=request.user.id).order_by('-orderDate')

    context = {
        'orders': orders,
        'menu': menu,
        'user': request.user
    }

    template = loader.get_template('store/user.html')
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
    template = loader.get_template('store/register.html')
    return HttpResponse(template.render({}, request))

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
    try:
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
    except ObjectDoesNotExist:
        return redirect('login_page')

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
        user = User.objects.get(pk=request.user.id)
        order = Order(owner=user, totalPrice=cart.total_price(), orderNumber=uuid.uuid4())
        order.save()
        order.products.set(cart.products.all())
        order.save()

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
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            payment_method_types=[
              'card'
            ],
            mode='payment',
            success_url = YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}' + '&orderNumber=' + str(order.orderNumber),
            cancel_url=YOUR_DOMAIN + '/cancel',
        )

        cart = Cart.objects.get(owner=request.user.id)
        cart.products.clear()
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
