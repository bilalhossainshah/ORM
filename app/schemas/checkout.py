"""
Checkout and Shipping related schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ShippingAddress(BaseModel):
    """Shipping address schema"""
    full_name: str
    email: EmailStr
    phone_number: str
    street_address: str
    city: str
    state: str
    postal_code: str
    country: str


class CheckoutRequest(BaseModel):
    """Checkout request with shipping and payment info"""
    order_id: int
    shipping_address: ShippingAddress
    payment_method: str  # "stripe", "paypal", "cod" (cash on delivery)


class PaymentIntent(BaseModel):
    """Payment intent creation"""
    order_id: int
    amount: float  # in cents for Stripe
    currency: str = "usd"


class PaymentConfirmation(BaseModel):
    """Payment confirmation response"""
    payment_id: str
    order_id: int
    status: str  # "succeeded", "pending", "failed"
    amount: float
    timestamp: datetime


class OrderConfirmation(BaseModel):
    """Final order confirmation"""
    order_id: int
    status: str
    shipping_address: ShippingAddress
    estimated_delivery: str
    tracking_number: Optional[str] = None
