from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total', 'delivery', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'id']
    ordering = ['-created_at']
    readonly_fields = ['total', 'created_at', 'updated_at']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'product', 'quantity', 'price', 'subtotal', 'created_at']
    list_filter = ['created_at']
    search_fields = ['order__id', 'product__title']
    ordering = ['-created_at']
    readonly_fields = ['subtotal', 'created_at'] 