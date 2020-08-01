from django.contrib import admin
from .models import OrderItem, Order

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("items",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "ordered")