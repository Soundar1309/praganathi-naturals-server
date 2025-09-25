"""
Payment views for Razorpay integration.
"""

import uuid
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from decouple import config

from .models import Payment
from .serializers import CreateOrderSerializer, VerifyPaymentSerializer, PaymentSerializer
from .razorpay_client import create_order, verify_payment_signature
from orders.models import Order

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_razorpay_order(request):
    """
    Create a Razorpay order for payment processing.
    
    Expected payload:
    {
        "amount": 100.00,
        "currency": "INR",
        "order_id": 123 (optional)
    }
    """
    serializer = CreateOrderSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        amount = serializer.validated_data['amount']
        currency = serializer.validated_data.get('currency', 'INR')
        order_id = serializer.validated_data.get('order_id')
        
        # Convert amount to paise for Razorpay
        amount_in_paise = int(amount * 100)
        
        # Generate receipt ID
        receipt_id = f"receipt_{uuid.uuid4().hex[:8]}"
        
        # Create Razorpay order
        razorpay_order = create_order(
            amount=amount_in_paise,
            currency=currency,
            receipt=receipt_id
        )
        
        # Get order instance if order_id provided
        order_instance = None
        if order_id:
            try:
                order_instance = Order.objects.get(id=order_id, user=request.user)
            except Order.DoesNotExist:
                return Response(
                    {'error': 'Order not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Create payment record
        payment = Payment.objects.create(
            razorpay_order_id=razorpay_order['id'],
            amount=amount,
            currency=currency,
            user=request.user,
            order=order_instance
        )
        
        # Return response with Razorpay order details
        response_data = {
            'order_id': razorpay_order['id'],
            'amount': razorpay_order['amount'],
            'currency': razorpay_order['currency'],
            'receipt': razorpay_order['receipt'],
            'status': razorpay_order['status'],
            'payment_id': payment.id
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to create order: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    """
    Verify Razorpay payment signature and update payment status.
    
    Expected payload:
    {
        "razorpay_order_id": "order_xxx",
        "razorpay_payment_id": "pay_xxx",
        "razorpay_signature": "signature_xxx"
    }
    """
    serializer = VerifyPaymentSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        razorpay_order_id = serializer.validated_data['razorpay_order_id']
        razorpay_payment_id = serializer.validated_data['razorpay_payment_id']
        razorpay_signature = serializer.validated_data['razorpay_signature']
        
        # Get payment record
        try:
            payment = Payment.objects.get(
                razorpay_order_id=razorpay_order_id,
                user=request.user
            )
        except Payment.DoesNotExist:
            return Response(
                {'error': 'Payment not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verify payment signature
        is_signature_valid = verify_payment_signature(
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature
        )
        
        if is_signature_valid:
            # Update payment record
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'completed'
            payment.save()
            
            # Update order status if payment is associated with an order
            if payment.order:
                payment.order.status = 'confirmed'
                payment.order.save()
            
            return Response({
                'success': True,
                'message': 'Payment verified successfully',
                'payment_id': payment.id,
                'status': payment.status
            }, status=status.HTTP_200_OK)
        else:
            # Update payment status to failed
            payment.status = 'failed'
            payment.save()
            
            return Response({
                'success': False,
                'message': 'Payment verification failed',
                'status': payment.status
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response(
            {'error': f'Payment verification failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_details(request, payment_id):
    """
    Get payment details by payment ID.
    """
    try:
        payment = Payment.objects.get(id=payment_id, user=request.user)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_payments(request):
    """
    Get all payments for the authenticated user.
    """
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)