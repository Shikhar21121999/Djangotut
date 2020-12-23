# here we define forms for our models
# we use models form which link to our data models

from .models import *
from django.forms import ModelForm


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']
