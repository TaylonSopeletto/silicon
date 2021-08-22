from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login_page', views.login_page, name='login_page'),
    path('register_page', views.register_page, name='register_page'),
    path('authentication', views.authentication, name='authentication'),
    path('create_user', views.create_user, name='create_user'),
    path('product/<int:product_id>/', views.product, name='product'),

    path('cart', views.cart, name='cart'),
    path('add_product', views.addProduct, name='add_product'),
    path('remove_product', views.removeProduct, name='remove_product'),

    path('checkout', views.checkout, name='checkout'),
    path('create-checkout-session', views.create, name='create')
]