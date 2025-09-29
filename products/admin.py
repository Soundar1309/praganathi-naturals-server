from django.contrib import admin
from .models import Category, Product, ProductVariation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']




class ProductVariationInline(admin.TabularInline):
    """Inline admin for ProductVariation"""
    model = ProductVariation
    extra = 1
    fields = ['quantity', 'unit', 'price', 'original_price', 'stock', 'image', 'is_active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'display_name', 'price', 'original_price', 'stock', 'is_active', 'created_at']
    list_filter = ['unit', 'is_active', 'created_at']
    search_fields = ['product__title', 'quantity', 'unit']
    ordering = ['product', 'quantity', 'unit']
    readonly_fields = ['created_at', 'updated_at', 'has_offer', 'discount_percentage', 'display_name']
    fieldsets = (
        ('Basic Information', {
            'fields': ('product', 'quantity', 'unit', 'image')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price')
        }),
        ('Inventory', {
            'fields': ('stock', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Calculated Fields', {
            'fields': ('has_offer', 'discount_percentage', 'display_name'),
            'classes': ('collapse',)
        }),
    )


# Update ProductAdmin to include variations inline
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'original_price', 'offer_price', 'stock', 'available', 'has_offer', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'has_offer', 'discount_percentage']
    inlines = [ProductVariationInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'image')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price', 'offer_price')
        }),
        ('Inventory', {
            'fields': ('stock',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Calculated Fields', {
            'fields': ('has_offer', 'discount_percentage'),
            'classes': ('collapse',)
        }),
    ) 