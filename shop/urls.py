from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile, name='profile'),
    path('orders/', views.order_list, name='orders'),

    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),

    # ✅ Add these two:
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
