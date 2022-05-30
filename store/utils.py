import json
from .models import *
from django.contrib.auth.models import User

def cookieCart(request):

    ## if not authenticated
    ## get cookie name and assign it to another variable. so that we can manipulate cookie data

    ## When page loads for the first time. if no cookie is available then set cart to empty dictionary/object
    try:
        cart = request.COOKIES['cart'] ## 'cart' is a cookie name in main.html template and this is string data right now
    except:
        cart = {}

    # cart = json.loads(cart) ## will be in python dictionary

    items = []
    order = {'get_total_cart_items': 0, 'get_total_cart_price': 0}
    cartItems = order['get_total_cart_items']

## total items and price in cart (When user is not logged in)
    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_total_cart_price'] += total
            order['get_total_cart_items'] += cart[i]['quantity']

            ## showing items in cart with all details. 
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image': product.image
                },
                'quantity': cart[i]['quantity'],
                'get_total_price': total
            }
            items.append(item)

            # if product is physical
            if product.digital == False:
                order['shippping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    # Checking whether user is authinticated or not
    if request.user.is_authenticated:
        new_cust = request.user
        customer, created = Customer.objects.get_or_create(user = new_cust, name=new_cust, email=new_cust)
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitems_set.all() 
        cartItems = order.get_total_cart_items ## to get the total item in cart for cart icon badge in navbar
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']    
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}

# def guestOrder(request, data):

# 	name = data['form']['name']
# 	email = data['form']['email']

# 	cookieData = cookieCart(request)
# 	items = cookieData['items']

# 	customer, created = Customer.objects.get_or_create(
# 			email=email,
# 			)
# 	customer.name = name
# 	customer.save()

# 	order = Order.objects.create(
# 		customer=customer,
# 		complete=False,
# 		)

# 	for item in items:
# 		product = Product.objects.get(id=item['id'])
# 		orderItem = OrderItems.objects.create(
# 			product=product,
# 			order=order,
# 			quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']), # negative quantity = freebies
# 		)
# 	return customer, order


