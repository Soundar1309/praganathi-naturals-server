from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total', 'item_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email']
    ordering = ['-created_at']
    readonly_fields = ['total', 'item_count', 'created_at', 'updated_at']
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'subtotal', 'created_at']
    list_filter = ['created_at']
    search_fields = ['cart__user__email', 'product__title']
    ordering = ['-created_at']
    readonly_fields = ['subtotal', 'created_at', 'updated_at'] 