from django.contrib import admin

# Register your models here.
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Customer, CustomerAdmin)

# admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(Tag)
