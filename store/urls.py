from django.urls import path
from . import views
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', updateItem, name='update-item'),
    path('process_order/', processOrder, name='process-order'),
    # path('<slug>/', get_product, name='get-product'),
]

