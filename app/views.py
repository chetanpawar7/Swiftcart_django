from django.shortcuts import render
from . import models 
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect,get_object_or_404
from django.views import View
from django.db.models import Q
# razorpay
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.
def search_prod(request):
    query = request.GET.get('query')
    if query:
        product = models.Product.objects.all().filter(name__icontains=query)
    else:
        product = models.Product.objects.none()
    context ={
        "query":query,
        "product": product
    }
    return render(request, 'search_prod.html',context)


def index(request):
    return render(request, 'index.html')

def customerlogin(request):
    if request.method=='POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request,username =username,password = pass1)
        if user is not None:
            login(request,user)
            return redirect('store')
        else:
            return HttpResponse("username and password incorrect")
    return render(request, "customerlogin.html")

def customersignup(request):
    if request.method=='POST':
         uname = request.POST.get('username')
         email = request.POST.get('email')
         pass1 = request.POST.get('password')
         pass2 = request.POST.get('confirm_password')
         if pass1!=pass2:
             return HttpResponse("Password doesn't match..!")
         else:
             my_user=User.objects.create_user(uname,email,pass1)
             my_user.save()
             return redirect('customerlogin')
    return render(request, "customersignup.html")

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required(login_url='customerlogin')
def store(request):
    product = models.Product.objects.all()
    context={
        "product": product
    }
    
    return render(request, 'store.html',context)

@login_required(login_url='customerlogin')
def mobile(request):
    product = models.Product.objects.filter(category="MOBILE")
    context={
        "product": product
    }
    return render(request, 'mobile.html',context)

@login_required(login_url='customerlogin')
def electronics(request):
    product = models.Product.objects.filter(category="ELECTRONIC")
    context={
        "product": product
    }
    return render(request, 'electronics.html',context)

@login_required(login_url='customerlogin')
def fashion(request):
    product = models.Product.objects.filter(category ="FASHION")
    context={
        'product':product
    }
    return render(request, 'fashion.html',context)

@login_required(login_url='customerlogin')
def appliance(request):
    product = models.Product.objects.filter(category ="APPLIANCE")
    context={
        'product':product
    }
    return render(request, 'appliance.html',context)

def about(request):
    return render(request, 'about.html')

@login_required(login_url='customerlogin')
def cart(request):
    user = request.user
    if user.is_authenticated:
        cart = models.Cart.objects.all().filter(user=user)
    else:
        cart = models.Cart.objects.all()
    context ={
        "cart": cart
    }
    return render(request, "cart.html",context)

@login_required(login_url='customerlogin')
def add_to_cart(request,product_id):
    if request.method=='POST':
        product = models.Product.objects.get(id = product_id)

        cart_item = models.Cart.objects.filter(user = request.user,product=product).first()
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            models.Cart.objects.create(user = request.user, product=product)
        messages.success(request, 'added item successfully..!')
        return redirect('store')
    else:
        product = models.Product.objects.get(id = product_id)
        return render(request, 'store.html',{'product':product})

@login_required(login_url='customerlogin')
def remove_from_cart(request,product_id):
    if request.method=='POST':
        cart = models.Cart.objects.get(user= request.user,id=product_id)
        cart.delete()
    messages.success(request, ' item deleted successfully..!')
    return redirect('cart')


@login_required(login_url='customerlogin')
def edit_profile(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id = customer.user.id )
    if request.method =='POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        customer.mobile = request.POST['mobile']
        customer.locality = request.POST['locality']
        customer.city = request.POST['city']
        customer.state = request.POST['state']
        customer.zipcode = request.POST['zipcode']
        profile_image = request.FILES.get('profile_image') # profile photo updation problem
        if profile_image:
            customer.profile_image = profile_image
        customer.save()
        messages.success(request, 'profile updated successfully..!')
        return redirect('edit_profile')
    context = {
        "customer":customer
    }
    return render(request, 'edit_profile.html',context)

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required(login_url='customerlogin')
@csrf_exempt
def checkout(request):
    user = request.user
    customer = models.Customer.objects.filter(user=user)
    cart = models.Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.total
    amt= total_price
    currency = 'INR'
    amount = amt *100  # Rs. 200
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/payment_success/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'checkout.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
from .models import Order
@login_required(login_url='customerlogin')
@csrf_exempt
def payment_success(request):
	user = request.user
	cartid = models.Cart.objects.filter(user = user)
	customer =models.Customer.objects.get(user_id=user.id)
	print(customer)
	for cid in cartid:
		Order(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
		print("Order Saved")
		cid.delete()
		print("Cart Item Deleted")
	return redirect("orders")

@login_required(login_url='customerlogin')
def orders(request):
    user = request.user
    orderss1=models.Order.objects.all()
    if user.is_authenticated:
        orderss1 = models.Order.objects.all().filter(user=user)
    else:
        orderss1 = models.Orders.objects.all()
    context ={
        "orderss1": orderss1
    }
    return render(request, 'orders.html',context)

