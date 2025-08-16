from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import WishlistItem
from .serializers import WishlistItemSerializer
from products.models import Product

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    """Get user's wishlist"""
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    serializer = WishlistItemSerializer(wishlist_items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    try:
        # Check if product exists
        product = get_object_or_404(Product, id=product_id)
        
        # Check if already in wishlist
        if WishlistItem.objects.filter(user=request.user, product=product).exists():
            return Response(
                {"detail": "Product is already in your wishlist"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create wishlist item
        wishlist_item = WishlistItem.objects.create(
            user=request.user,
            product=product
        )
        
        # Update user's wishlist field
        if product_id not in request.user.wishlist:
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
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    try:
        # Find and delete wishlist item
        wishlist_item = get_object_or_404(
            WishlistItem, 
            user=request.user, 
            product_id=product_id
        )
        wishlist_item.delete()
        
        # Update user's wishlist field
        if product_id in request.user.wishlist:
            request.user.wishlist.remove(product_id)
            request.user.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    except Exception as e:
        return Response(
            {"detail": str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_wishlist_status(request, product_id):
    """Check if a product is in user's wishlist"""
    is_in_wishlist = WishlistItem.objects.filter(
        user=request.user, 
        product_id=product_id
    ).exists()
    
    return Response({"is_in_wishlist": is_in_wishlist})
