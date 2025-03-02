from django.urls import path

from . import views

urlpatterns = [
    #public
    path('', views.index, name='index'),
    path('product/<str:product_id>/', views.product, name='product'),
    
    #user
    path('user', views.user, name='user'),
    path('login_page', views.login_page, name='login_page'),
    path('authentication', views.authentication, name='authentication'),
    path('register_page', views.register_page, name='register_page'),
    path('logout', views.logout_view, name='logout'),
    #cart
    path('cart', views.cart, name='cart'),
    path('add_product', views.addProduct, name='add_product'),
    path('remove_product', views.removeProduct, name='remove_product'),
    #order
    path('cancel', views.cancel_payment, name='cancel'),
    path('success', views.success_payment, name='success'),
    path('create-checkout-session', views.create, name='create')
]