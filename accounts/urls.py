
from django.contrib import admin
from django.urls import path  # basic libraries to be included
from . import views     # importing views from the current directory

urlpatterns = [
    path('dashboard/', views.home),
    path('products/', views.products),
    path('customers/', views.customers)
]
