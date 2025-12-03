# app/models/__init__.py

# Import all model classes from their respective files
# This makes them visible to SQLAlchemy's metadata system
from .category import Category
from .product import Product
from .user import User
from .cart import Order, OrderItem

# You can optionally define __all__ if you plan on using 
# "from app.models import *" in other places, but the imports above 
# are sufficient to resolve your current error in main.py
__all__ = [
    "Category",
    "Product",
    "User",
    "Order",
    "OrderItem"
]
