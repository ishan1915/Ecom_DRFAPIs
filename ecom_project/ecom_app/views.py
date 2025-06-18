from django.http import HttpResponse,HttpResponseForbidden
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Product, Order, User
from .serializers import UserSerializer, ProductSerializer, OrderSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import ProductForm,OrderForm

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


def signup(request):
    return render(request, 'signup.html')

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        if user.is_seller:
            return redirect('/api/seller/dashboard/')
        else:
            return redirect('/api/buyer/dashboard/')
    return Response({'error': 'Invalid credentials'}, status=400)

def login(request):
    return render(request, 'login.html')



class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['category', 'price']

@login_required
def ProductView(request):
    query = request.GET.get('search')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()
    return render(request, 'product.html', {'products': products, 'query': query})

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer




@login_required
def product_add(request):
    if not request.user.is_seller:
        return HttpResponse("Only sellers can add products", status=403)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('/api/seller/dashboard/')
    else:
        form = ProductForm()
    return render(request, 'productadd.html', {'form': form})



@login_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    buyers = User.objects.filter(order__product__seller=request.user).distinct()
    return render(request, 'seller_dashboard.html', {'products': products, 'buyers': buyers})

@login_required
def buyer_dashboard(request):
    orders = Order.objects.filter(buyer=request.user).select_related('product')
    return render(request, 'buyer_dashboard.html', {'orders': orders, 'user': request.user})

@api_view(['POST'])
def create_order(request):
    if not request.user.is_authenticated or request.user.is_seller:
        return Response({'error': 'Only buyers can place orders.'}, status=403)
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(buyer=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@login_required
def create_order_view(request):
    if request.user.is_seller:
        return HttpResponseForbidden("Only buyers can place orders.")
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.buyer = request.user
            order.save()
            return redirect('/api/buyer/dashboard/')
    else:
        form = OrderForm()
    
    return render(request, 'create_order.html', {'form': form})