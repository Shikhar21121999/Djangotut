from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm
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
    return render(request, 'accounts/customers.html', {'customer': customer, 'orders': order_lis, 'order_cnt': order_cnt})


def products(request):
    product_lis = Products.objects.all()
    return render(request, 'accounts/products.html', {'prod_lis': product_lis})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = OrderForm()
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    form = OrderForm(instance=order)
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        print("deleting order")
        order.delete()
        return redirect('home')
    return render(request, 'accounts/delete_order.html', {'order':order})
