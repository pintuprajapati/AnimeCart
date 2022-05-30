from django.urls import path
from . import views
from .views import *

from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('login/', login_user, name='login_user'),
    path('register/', register_user, name='register_user'),
    path('logout/', logout_user, name='logout_user'),
]

