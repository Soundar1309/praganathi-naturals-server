from django.contrib import admin
from django.db.models import Q, F
from django.utils.html import format_html
from .models import Category, Product, ProductVariation


class StockRangeFilter(admin.SimpleListFilter):
    title = 'stock range'
    parameter_name = 'stock_range'

    def lookups(self, request, model_admin):
        return (
            ('out_of_stock', 'Out of Stock (0)'),
            ('low_stock', 'Low Stock (1-10)'),
            ('medium_stock', 'Medium Stock (11-50)'),
            ('high_stock', 'High Stock (51+)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'out_of_stock':
            return queryset.filter(stock=0)
        elif self.value() == 'low_stock':
            return queryset.filter(stock__range=(1, 10))
        elif self.value() == 'medium_stock':
            return queryset.filter(stock__range=(11, 50))
        elif self.value() == 'high_stock':
            return queryset.filter(stock__gt=50)


class PriceRangeFilter(admin.SimpleListFilter):
    title = 'price range'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('under_100', 'Under ₹100'),
            ('100_500', '₹100 - ₹500'),
            ('500_1000', '₹500 - ₹1000'),
            ('over_1000', 'Over ₹1000'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'under_100':
            return queryset.filter(price__lt=100)
        elif self.value() == '100_500':
            return queryset.filter(price__range=(100, 500))
        elif self.value() == '500_1000':
            return queryset.filter(price__range=(500, 1000))
        elif self.value() == 'over_1000':
            return queryset.filter(price__gt=1000)


class OfferStatusFilter(admin.SimpleListFilter):
    title = 'offer status'
    parameter_name = 'offer_status'

    def lookups(self, request, model_admin):
        return (
            ('has_offer', 'Has Offer'),
            ('no_offer', 'No Offer'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'has_offer':
            return queryset.filter(original_price__gt=F('price'))
        elif self.value() == 'no_offer':
            return queryset.filter(Q(original_price=F('price')) | Q(original_price__isnull=True))


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
    list_display = ['title', 'category', 'price', 'original_price', 'offer_price', 'stock', 'available', 'has_offer', 'product_type', 'is_in_stock', 'created_at']
    list_filter = [
        'category', 
        'product_type', 
        'is_in_stock',
        OfferStatusFilter,
        StockRangeFilter,
        PriceRangeFilter,
        ('created_at', admin.DateFieldListFilter),
        ('updated_at', admin.DateFieldListFilter),
    ]
    search_fields = ['title', 'description', 'category__name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'has_offer', 'discount_percentage']
    inlines = [ProductVariationInline]
    list_per_page = 25
    list_select_related = ['category']
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