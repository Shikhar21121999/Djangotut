from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.

# here we create function which will be called through urls file


def home(request):
    customer_lis = Customer.objects.all()
    order_lis = Order.objects.all()
    total_order = order_lis.count()
    order_delivered = order_lis.filter(status="Delivered").count()
    order_pending = order_lis.filter(status="Pending").count()
    return render(request, 'accounts/dashboard.html',
                  {'cus_lis': customer_lis, 'order_lis': order_lis,
                   'order_delivered': order_delivered, 'order_pending': order_pending,
                   'total_order': total_order}
                  )


def customers(request, cus_id):
    customer = Customer.objects.get(id=cus_id)
    order_lis = Order.objects.filter(customer=customer)
    order_cnt = order_lis.count()
    myfilter = OrderFilter(request.GET, queryset=order_lis)
    order_lis = myfilter.qs
    context = {'customer': customer,
               'orders': order_lis, 'order_cnt': order_cnt, 'myfilter': myfilter}
    return render(request, 'accounts/customers.html', context)


def products(request):
    product_lis = Products.objects.all()
    return render(request, 'accounts/products.html', {'prod_lis': product_lis})


def create_order(request, cus_id):
    OrderFormset = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=cus_id)
    formset = OrderFormset(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = OrderFormset(request.POST, instance=customer)
        if formset.is_valid():
            # new_order = form.save(commit=False)
            # new_order.customer = customer
            formset.save()
            return redirect('home')
    context = {'formset': formset, 'customer': customer}
    return render(request, 'accounts/order_formset.html', context)


def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    form = OrderForm(instance=order)
    context = {'form': form, 'order': order}
    return render(request, 'accounts/order_form.html', context)


def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        print("deleting order")
        order.delete()
        return redirect('home')
    return render(request, 'accounts/delete_order.html', {'order': order})


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        print("submitting form")
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print("form is valid")
            form.save()
            new_user = form.cleaned_data.get('username')
            # messages.success(request, 'Profile details updated.')
            messages.success(
                request, 'Account was created successfully for user '+new_user)
            return redirect('login')
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    return render(request, 'accounts/login.html')
