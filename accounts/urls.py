
from django.contrib import admin
from django.urls import path  # basic libraries to be included
from . import views     # importing views from the current directory

urlpatterns = [
    path('dashboard/', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customers/<str:cus_id>/', views.customers, name="customer"),
    path('create_order/<str:cus_id>/', views.create_order, name="create_order"),
    path('update_order/<str:order_id>/',
         views.update_order, name="update_order"),
    path('delete_order/<str:order_id>/',
         views.delete_order, name="delete_order"),
    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.user_logout, name="logout"),
    path('user/', views.user_home, name="user"),
    path('user_settings', views.user_settings, name="user_settings")
]
