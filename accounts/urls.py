
from django.contrib import admin
from django.urls import path  # basic libraries to be included
from . import views     # importing views from the current directory

urlpatterns = [
    path('dashboard/', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customers/<str:cus_id>/', views.customers, name="customer"),
    path('create_order/', views.create_order, name="create_order"),
    path('update_order/<str:order_id>/',
         views.update_order, name="update_order"),
    path('delete_order/<str:order_id>/',
         views.delete_order, name="delete_order"),
]
