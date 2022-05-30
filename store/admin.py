from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ShippingAddress)

## custom visual representaion of 'Product' model in admin panel 

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email']
    model = Customer

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'digital', 'description', 'slug', 'image', 'price']
    model = Product

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity',]
    model = OrderItems

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'complete', 'transaction_id']
    model = Order
