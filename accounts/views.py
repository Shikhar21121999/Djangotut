from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user_group
from django.contrib.auth.models import Group
# Create your views here.

# here we create function which will be called through urls file


@login_required(login_url='login')
@allowed_user_group(allowed_roles=['admin'])
def home(request):
    '''
    dash board view acessible only to memeber of admin
    '''

    customer_lis = Customer.objects.all()
    order_lis = Order.objects.all()
    total_order = order_lis.count()

    order_delivered = order_lis.filter(status="Delivered").count()
    order_pending = order_lis.filter(status="Pending").count()

    context = {'cus_lis': customer_lis,
               'order_lis': order_lis,
               'order_delivered': order_delivered, 'order_pending': order_pending,
               'total_order': total_order}

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_user_group(allowed_roles=['customer'])
def user_home(request):
    '''
    dashboard view for a customer user
    belonging to group customer
    '''

    # getting orders for current user using customer relation
    orders = request.user.customer.order_set.all()
    total_order = orders.count()

    order_delivered = orders.filter(status="Delivered").count()
    order_pending = orders.filter(status="Pending").count()

    context = {
        'orders': orders,
        'order_delivered': order_delivered,
        'order_pending': order_pending,
        'total_order': total_order

    }

    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_user_group(allowed_roles=['admin'])
def customers(request, cus_id):
    '''
    customer view showing order information about a particular user
    acessible only to a logged in user who is a member of admin group
    '''

    customer = Customer.objects.get(id=cus_id)
    order_lis = Order.objects.filter(customer=customer)
    order_cnt = order_lis.count()

    myfilter = OrderFilter(request.GET, queryset=order_lis)
    order_lis = myfilter.qs

    context = {'customer': customer,
               'orders': order_lis, 'order_cnt': order_cnt, 'myfilter': myfilter}
    return render(request, 'accounts/customers.html', context)


@login_required(login_url='login')
@allowed_user_group(allowed_roles=['admin'])
def products(request):
    '''
    product view showing product information
    acessible only to admin
    '''
    product_lis = Products.objects.all()
    return render(request, 'accounts/products.html', {'prod_lis': product_lis})


@login_required(login_url='login')
@allowed_user_group(allowed_roles=['customer'])
def create_order(request, cus_id):
    '''
    a form view used to create a new order
    it uses inlineformset_factory to create a form with multiple forms
    '''
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


@login_required(login_url='login')
@allowed_user_group(allowed_roles=['customer'])
def update_order(request, order_id):
    '''
    a form view used to update an order
    it uses inlineformset_factory to create a form with multiple forms
    '''

    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect('home')

    form = OrderForm(instance=order)
    context = {'form': form, 'order': order}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_user_group(allowed_roles=['customer'])
def delete_order(request, order_id):
    '''
    view method to confirm deletion of an order
    '''

    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        print("deleting order")

        order.delete()
        return redirect('home')

    return render(request, 'accounts/delete_order.html', {'order': order})


@unauthenticated_user
def register(request):
    '''
    view method to register a new user
    initially it adds a new user to customer group
    view function acessible only to unauthenticated_user
    '''

    form = CreateUserForm()

    if request.method == 'POST':
        print("submitting form")

        form = CreateUserForm(request.POST)
        if form.is_valid():

            print("form is valid")
            new_user = form.save()  # returns the user object
            user_name = form.cleaned_data.get('username')

            # add new_user to group customer
            group = Group.objects.get(name='customer')
            new_user.groups.add(group)

            # create a new customer which has relation to current_user
            Customer.objects.create(user=new_user)

            # messages.success(request, 'Profile details updated.')
            messages.success(
                request, 'Account was created successfully for user '
                + user_name)
            return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def user_login(request):
    '''
    view to log in and authenticate a user in
    user is redirected to dashboard if belonging to admin group
    view function acessible only to unauthenticated_user
    '''

    if request.method == 'POST':
        # get the username and password
        # authenticate user with passowrd and log it in
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            login(request, user)
            # if the user is admin redirect to 'home'
            # that is the dashboard
            if user.groups.filter(name='admin').exists():
                print(user, 'belongs to admin group')
                return redirect('home')
            # in this case we explicitly assume that it belongs
            # to customer group
            else:
                print(user, 'not admin')
                return redirect('user')

        else:
            print('login failed for user: ', username, password)
            messages.info(request, 'username or passowrd is incorrect')
            return redirect('login')

    return render(request, 'accounts/login.html')


def user_logout(request):
    '''
    view method to log a user out
    '''

    print("logging out ", request.user.username)
    user_logged_out = request.user.username

    logout(request)
    messages.success(
        request, 'user sucessfully logged out')
    return redirect('login')
