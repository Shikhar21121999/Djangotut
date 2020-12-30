# here we define forms for our models
# we use models form which link to our data models
from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth


class CustomerForm(ModelForm):
    '''
    class to create a form for customer
    which will be used to update changes in the
    customer settings
    '''
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class OrderForm(ModelForm):
    '''
    class to  create a form for order placed by customer
    '''
    class Meta:
        model = Order
        fields = ['status']


class CreateUserForm(UserCreationForm):
    '''
    class to create a form for django model user
    '''
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.fields.TextInput(attrs={'placeholder': 'Username..'}),
            'email': forms.fields.TextInput(attrs={'placeholder': 'Email..'}),
        }
