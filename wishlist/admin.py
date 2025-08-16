from django.contrib import admin
from .models import WishlistItem

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at', 'user__role']
    search_fields = ['user__email', 'product__title']
    readonly_fields = ['added_at']
    ordering = ['-added_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'product')
