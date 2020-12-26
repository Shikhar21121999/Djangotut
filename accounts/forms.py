# here we define forms for our models
# we use models form which link to our data models
from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class CreateUserForm(UserCreationForm):
    class Meta:
        password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password from numbers and letters of the Latin alphabet'}))
        password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password confirm'}))
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.fields.TextInput(attrs={'placeholder': 'Username..'}),
            'email': forms.fields.TextInput(attrs={'placeholder': 'Email..'}),
        }

# class CreateUserForm(UserCreationForm):
#     first_name = forms.CharField(label="First name", widget=forms.TextInput(
#         attrs={'placeholder': "First name"}))
#     email = forms.EmailField(label="Email", widget=forms.TextInput(
#         attrs={'placeholder': "Email"}))

#     class Meta(UserCreationForm.Meta):
#         model = auth.get_user_model()
#         fields = [
#             'first_name',
#             'email',
#             'password1',
#             'password2'
#         ]

#     def __init__(self, *args, **kwargs):
#         super(InviteRegistrationForm, self).__init__(*args, **kwargs)
#         self.fields['password1'].widget = forms.PasswordInput(
#             attrs={'placeholder': "Password"})
#         self.fields['password2'].widget = forms.PasswordInput(
#             attrs={'placeholder': "Password"})
