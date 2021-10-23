from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Order,CartItem
# Register your models here.

admin.site.register(Order)
admin.site.register(CartItem)