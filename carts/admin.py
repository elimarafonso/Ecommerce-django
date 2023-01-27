from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ()


@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    list_display = ()