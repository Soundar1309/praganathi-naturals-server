from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import WishlistItem
from .serializers import WishlistItemSerializer
from products.models import Product

@api_view(['GET'])
@permission_classes([AllowAny])
def get_wishlist(request):
    """Get user's wishlist (authenticated or anonymous)"""
    wishlist_items = WishlistItem.get_user_wishlist(request)
    serializer = WishlistItemSerializer(wishlist_items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_to_wishlist(request, product_id):
    """Add product to wishlist (authenticated or anonymous)"""
    try:
        # Check if product exists
        product = get_object_or_404(Product, id=product_id)
        
        # Check if already in wishlist
        if WishlistItem.check_wishlist_status(request, product_id):
            return Response(
                {"detail": "Product is already in your wishlist"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create wishlist item
        wishlist_item = WishlistItem.get_or_create_wishlist_item(request, product)
        
        # Update user's wishlist field if authenticated
        if request.user.is_authenticated and product_id not in request.user.wishlist:
            request.user.wishlist.append(product_id)
            request.user.save()
        
        serializer = WishlistItemSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {"detail": str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['DELETE'])
@permission_classes([AllowAny])
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist (authenticated or anonymous)"""
    try:
        # Find and delete wishlist item
        if request.user.is_authenticated:
            wishlist_item = get_object_or_404(
                WishlistItem, 
                user=request.user, 
                product_id=product_id
            )
        else:
            # Ensure session exists and is saved
            if not request.session.session_key:
                request.session.create()
                request.session.save()
            
            session_key = request.session.session_key
            wishlist_item = get_object_or_404(
                WishlistItem, 
                session_key=session_key, 
                product_id=product_id
            )
        
        wishlist_item.delete()
        
        # Update user's wishlist field if authenticated
        if request.user.is_authenticated and product_id in request.user.wishlist:
            request.user.wishlist.remove(product_id)
            request.user.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    except Exception as e:
        return Response(
            {"detail": str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def check_wishlist_status(request, product_id):
    """Check if a product is in user's wishlist (authenticated or anonymous)"""
    is_in_wishlist = WishlistItem.check_wishlist_status(request, product_id)
    return Response({"is_in_wishlist": is_in_wishlist})
