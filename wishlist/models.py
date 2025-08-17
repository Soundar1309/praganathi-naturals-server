from django.db import models
from django.conf import settings

class WishlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist_items', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='wishlist_items')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'product', 'session_key']
        ordering = ['-added_at']
    
    def __str__(self):
        if self.user:
            return f"{self.user.email} - {self.product.title}"
        else:
            return f"Anonymous - {self.product.title}"
    
    @classmethod
    def get_or_create_wishlist_item(cls, request, product):
        """Get or create wishlist item for authenticated or anonymous user"""
        if request.user.is_authenticated:
            wishlist_item, created = cls.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'session_key': None}
            )
        else:
            # Ensure session exists and is saved
            if not request.session.session_key:
                request.session.create()
                request.session.save()
            
            session_key = request.session.session_key
            wishlist_item, created = cls.objects.get_or_create(
                session_key=session_key,
                product=product,
                defaults={'user': None}
            )
        return wishlist_item
    
    @classmethod
    def get_user_wishlist(cls, request):
        """Get wishlist for authenticated or anonymous user"""
        if request.user.is_authenticated:
            return cls.objects.filter(user=request.user)
        else:
            # Ensure session exists and is saved
            if not request.session.session_key:
                request.session.create()
                request.session.save()
            
            session_key = request.session.session_key
            return cls.objects.filter(session_key=session_key)
    
    @classmethod
    def check_wishlist_status(cls, request, product_id):
        """Check if a product is in user's wishlist"""
        if request.user.is_authenticated:
            return cls.objects.filter(user=request.user, product_id=product_id).exists()
        else:
            # Ensure session exists and is saved
            if not request.session.session_key:
                request.session.create()
                request.session.save()
            
            session_key = request.session.session_key
            return cls.objects.filter(session_key=session_key, product_id=product_id).exists()
