from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse
import json
import datetime
from .utils import cookieCart, cartData
from django.contrib.auth.decorators import login_required

# Create your views here.
def store(request):
    cart_data = cartData(request)
    cartItems = cart_data['cartItems']

    all_products = Product.objects.all()
    context = {'products': all_products, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/store.html', context)

@login_required(login_url='/accounts/login')
def cart(request):
    cart_data = cartData(request)
    cartItems = cart_data['cartItems']    
    order = cart_data['order']
    items = cart_data['items']   

    context = {'items': items, 'order': order,  'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/cart.html', context)

@login_required(login_url='/accounts/login')
def checkout(request):
    cart_data = cartData(request)
    cartItems = cart_data['cartItems']    
    order = cart_data['order']
    items = cart_data['items']


    context = {'items': items, 'order': order,  'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

## This function is available when user is logged in
@login_required(login_url='/accounts/login')
def updateItem(request):
    data_1 = request.body
    # print('data_1:', data_1)

    data = json.loads(data_1)
    # print('data:', data)

    productId = data['productId']
    action = data['action']


    customer = request.user.customer ## logged in customer
    product =  Product.objects.get(id=productId)

    ## getting the order/cart attached to customer which has value of complete=False
    order, created = Order.objects.get_or_create(customer = customer, complete = False)

    ## if the item already exist, according to product in order/cart -> then increase the quantity only 
    orderItem, created = OrderItems.objects.get_or_create(order=order, product=product) 

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    ## if quantity is <=0 then delete the item from cart
    if orderItem.quantity <= 0:
        orderItem.delete()
    

    return JsonResponse('Item was added', safe=False)

## payment process -> If payment is successful then cart Items will be zero.
@login_required(login_url='/accounts/login')
def processOrder(request):
    transaction_id =datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        print(order, created)
        total = data['form']['total']
        order.transaction_id = transaction_id

        ## if the total of form is same as total_cart_price then 
        if int(total) == int(order.get_total_cart_price):
            order.complete = True ## after this -> cart items will be ZERO
        order.save() ## regardless of complete is True of Flase. save the order

        ## Shipping Data -> If item is physical then shipping is True (from Order Model)
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
    else:
        print('user not logged in')
        # pass
    return JsonResponse('Payment Complete', safe=False)

# Show the details of individual product/item
#  <a href="{% url 'get-product' product.slug %}" class="btn btn-primary mt-2 expand-view">View</a> 
# add above line for 'view button' in 'store.html'
def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {'product': product}

        return render(request, 'store/product_details.html', context)
    except Exception as e:
        print(e)