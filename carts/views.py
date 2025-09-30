from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from decimal import Decimal
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartView(generics.RetrieveAPIView):
    """Cart view equivalent to Rails CartsController"""
    serializer_class = CartSerializer
    permission_classes = []  # Allow anonymous users
    
    def get_object(self):
        # Get or create cart for the user (authenticated or anonymous)
        return Cart.get_or_create_cart(self.request)


class CartItemViewSet(generics.ListCreateAPIView):
    """CartItem views equivalent to Rails CartItemsController"""
    serializer_class = CartItemSerializer
    permission_classes = []  # Allow anonymous users
    
    def get_queryset(self):
        cart = Cart.get_or_create_cart(self.request)
        return CartItem.objects.filter(cart=cart).select_related('product')
    
    def perform_create(self, serializer):
        cart = Cart.get_or_create_cart(self.request)
        serializer.save(cart=cart)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """CartItem detail view"""
    serializer_class = CartItemSerializer
    permission_classes = []  # Allow anonymous users
    
    def get_queryset(self):
        cart = Cart.get_or_create_cart(self.request)
        return CartItem.objects.filter(cart=cart).select_related('product')
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        quantity = request.data.get('quantity', 1)
        custom_quantity = request.data.get('custom_quantity')
        custom_unit = request.data.get('custom_unit')
        
        # If custom quantity is provided, use it; otherwise use regular quantity
        if custom_quantity is not None and custom_unit:
            # Convert to Decimal if it's a string or float
            try:
                custom_quantity = Decimal(str(custom_quantity))
            except (ValueError, TypeError, Exception):
                return Response({'error': 'Invalid custom quantity'}, status=status.HTTP_400_BAD_REQUEST)
            
            if custom_quantity <= 0:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            instance.custom_quantity = custom_quantity
            instance.custom_unit = custom_unit
            # Reset regular quantity when using custom
            instance.quantity = 1
        else:
            if quantity <= 0:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            instance.quantity = quantity
            # Clear custom fields when using regular quantity
            instance.custom_quantity = None
            instance.custom_unit = None
        
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data) 