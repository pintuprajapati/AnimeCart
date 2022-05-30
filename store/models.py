from itertools import product
from statistics import mode
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True) ## one customer - user
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null = True, blank=True)
    description = models.TextField()
    price = models.IntegerField()
    digital = models.BooleanField(default=False, blank=False, null=True)
    image = models.ImageField(upload_to='store/product_images', default="")

    # To generate a slug based on product name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

## Order is Cart
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True) ## one customer - many orders - cart
    date_ordered = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.id)

    ## cart total
    @property
    def get_total_cart_price(self):
        orderitems = self.orderitems_set.all() ## used OrderItems model
        total_cart_price = sum([item.get_total_price for item in orderitems])
        return total_cart_price

    ## total quantity of OrderItems models (below)
    @property
    def get_total_cart_items(self):
        orderitems = self.orderitems_set.all()
        total_cart_quantity = sum([item.quantity for item in orderitems])
        return total_cart_quantity

    ## for shipping - Checking whether the item is digital or physical
    def shipping(self):
        shipping = False
        orderitems = self.orderitems_set.all()
        for item in orderitems:
            if item.product.digital == False:
                shipping = True
        return shipping

## OrderItems is Items within Cart
class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True) ## Items from Product
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True) ## child of order - Single order can have multiple OrderItems
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    ## total price of particular item (item_price * quantity)
    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

