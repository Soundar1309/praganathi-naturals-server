from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
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
        
        if quantity <= 0:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        instance.quantity = quantity
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data) 