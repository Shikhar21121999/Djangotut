from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# here we create function which will be called through urls file


def home(request):
    return render(request, 'accounts/dashboard.html')


def customers(request):
    return render(request, 'accounts/customers.html')


def products(request):
    return render(request, 'accounts/products.html')
