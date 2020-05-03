from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import createform_Order,createuserform,account_settingsform
from .filter import Orderfilter
from .decorators import unauthenticated_user,allowed_users,admin_only



# Create your views here.
@unauthenticated_user
def Register(request):
 
    form = createuserform()
    if request.method == 'POST':
        form = createuserform(request.POST)
        if form.is_valid():
            user =form.save()
            username = form.cleaned_data.get('username')
      
            messages.success(request,'Account was successfully created for ' + username )
            return redirect('login')


    context ={'form':form}
    return render(request,'register.html',context)


@unauthenticated_user    
def loginuser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request,'Username or password is incorrect')
            
    context = {}
    return render(request,'login.html',context)

def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_rolls=['customers'])
def userpage(request):
    orders =request.user.customers.orders_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='pending').count()
 
    context={'orders':orders,'total_orders': total_orders,'delivered':delivered,'pending':pending}
    return render(request,'user.html',context)

@login_required(login_url='login')
@admin_only
def index(request):
    customers = Customers.objects.all()
    orders = Orders.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='pending').count()
    out_of_delivery = orders.filter(status='out_of_delivery').count()

    content = {'customers':customers,'orders':orders,'total_orders': total_orders,'delivered':delivered,'pending':pending,'out_of_delivery':out_of_delivery}
    return render(request,'home.html',content)

@login_required(login_url='login')
@allowed_users(allowed_rolls=['admin'])
def products(request):

    products = Products.objects.all()

    return render(request,'products.html',{'products':products})


@login_required(login_url='login')
@allowed_users(allowed_rolls=['admin'])
def customer(request, pk_test):
    customers = Customers.objects.get(id=pk_test)
   
    orders = customers.orders_set.all()
    total_order = orders.count()
    orderfilters = Orderfilter(request.GET,queryset=orders)
    orders = orderfilters.qs

    context = {'customers':customers, 'orders':orders ,'total_order':total_order, 'orderfilters':orderfilters}
    return render(request,'customers.html',context)

@login_required(login_url='login')

def about(request):
    return render(request,'abouts.html')

@login_required(login_url='login')
@allowed_users(allowed_rolls=['customers'])
def accountsettings(request):
    customer = request.user.customers
    form = account_settingsform(instance=customer)
    if request.method == 'POST':
        form = account_settingsform(request.POST,request.FILES,instance=customer)
        if form.is_valid:
            form.save()

    context = {'form':form}
    return render(request, 'account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_rolls=['admin'])
def updatecustomerform(request):
    customer = request.user.customers
    form = account_settingsform(instance=customer)
    if request.method == 'POST':
        form = account_settingsform(request.POST,request.FILES,instance=customer)
        if form.is_valid:
            form.save()

    context = {'form':form}
    return render(request, 'update_customerform.html', context)


@login_required(login_url='login')
@admin_only
def createCustomer(request):
    form = createuserform()
    if request.method == 'POST':
        form = createuserform(request.POST)
        if form.is_valid():
            username= form.save()
            users = form.cleaned_data.get('username')
            messages.success(request,'Account was successfully created')
            
            return redirect('index')
    context = {'form':form}
    return render(request,'customerform.html',context)

@login_required(login_url='login')
@allowed_users(allowed_rolls=['admin'])
def createform(request,pk):

    OrderFormSet = inlineformset_factory(Customers,Orders, fields=('product','status'),extra=5)
    customer = Customers.objects.get(id=pk)
    formSet = OrderFormSet(queryset=Orders.objects.none(),instance=customer)
    if request.method == 'POST':
        formSet = OrderFormSet(request.POST,instance=customer)
        if formSet.is_valid():
                
            formSet.save()
            return redirect('index')

    context = {'formSet':formSet}

    return render(request,'forms.html',context)

@login_required(login_url='login')
@allowed_users(allowed_rolls=['admin'])
def updateform(request,pk):
    OrderFormSet = inlineformset_factory(Customers,Orders, fields=('__all__'),extra=0)
    customer = Customers.objects.get(id=pk)
    formSet = OrderFormSet(instance=customer)
    if request.method == 'POST':
        formSet = OrderFormSet(request.POST,instance=customer)
        if formSet.is_valid():
                
            formSet.save()
            return redirect('index')

    context = {'formSet':formSet}

    return render(request,'forms.html',context)

    '''
    OrderFormSet = inlineformset_factory(Customers,Orders, fields=('product','status'),extra=5)
    customer = Customers.objects.get(id=pk)
    formSet = OrderFormSet(queryset=Orders.objects.none(),instance=customer)
    #form = createform_Order()
    if request.method == 'POST':
        
        #form = createform_Order(request.POST,)
        formSet = OrderFormSet(request.POST,instance=customer)
        if formSet.is_valid():
                
            formSet.save()
            return redirect('index')

    context = {'formSet':formSet}

    return render(request,'forms.html',context)
    '''
@login_required(login_url='login')
@allowed_users(allowed_rolls=['admin'])
def delete_form(request,pk):
    order = Orders.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('index')

    context = {'item':order}

    return render(request,'delete_form.html',context)
    










