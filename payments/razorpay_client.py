"""
Razorpay client wrapper for Django application.
Handles Razorpay API interactions for payment processing.
"""

import razorpay
from django.conf import settings
from decouple import config

# Initialize Razorpay client with environment variables
RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID', default='rzp_live_RLH4P9d5sBsA4S')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET', default='oNikoihBTX45Q45wnRWO5QUc')

# Create Razorpay client instance
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def create_order(amount, currency='INR', receipt=None):
    """
    Create a Razorpay order.
    
    Args:
        amount (int): Amount in paise (e.g., 10000 for ₹100)
        currency (str): Currency code (default: INR)
        receipt (str): Receipt ID for the order
    
    Returns:
        dict: Razorpay order response
    """
    try:
        order_data = {
            'amount': amount,
            'currency': currency,
        }
        
        if receipt:
            order_data['receipt'] = receipt
            
        order = client.order.create(data=order_data)
        return order
    except Exception as e:
        raise Exception(f"Failed to create Razorpay order: {str(e)}")

def verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """
    Verify Razorpay payment signature.
    
    Args:
        razorpay_order_id (str): Order ID from Razorpay
        razorpay_payment_id (str): Payment ID from Razorpay
        razorpay_signature (str): Signature from Razorpay
    
    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        # Create the signature string
        signature_data = f"{razorpay_order_id}|{razorpay_payment_id}"
        
        # Verify the signature
        is_valid = client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
        
        return is_valid
    except Exception as e:
        print(f"Signature verification failed: {str(e)}")
        return False

def get_payment_details(payment_id):
    """
    Get payment details from Razorpay.
    
    Args:
        payment_id (str): Payment ID from Razorpay
    
    Returns:
        dict: Payment details from Razorpay
    """
    try:
        payment = client.payment.fetch(payment_id)
        return payment
    except Exception as e:
        raise Exception(f"Failed to fetch payment details: {str(e)}")
