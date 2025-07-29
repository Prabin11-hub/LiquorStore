from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Cart, CartItem, Order, Profile
from .forms import RegisterForm, CheckoutForm, ProfileForm
from django.contrib.auth.models import User


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(product=product)
    cart.items.add(cart_item)
    messages.success(request, "Item added to cart!")
    return redirect('cart')


@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    return render(request, 'cart.html', {'cart': cart})


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            order.items.set(cart.items.all())
            order.paid = True
            order.save()
            cart.items.clear()
            messages.success(request, "Order placed successfully!")
            return redirect('orders')
    else:
        form = OrderForm()
    return render(request, 'checkout.html', {'form': form, 'cart': cart})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            Profile.objects.create(user=user)  # Optional: create user profile
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'customer/profile.html', {'form': form})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})


@login_required
def customer_dashboard(request):
    return render(request, 'customer/dashboard.html')


@login_required
def vendor_dashboard(request):
    return render(request, 'vendor/dashboard.html')
