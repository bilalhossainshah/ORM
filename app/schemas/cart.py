
from decimal import ROUND_HALF_UP, Decimal
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: Decimal
    
def round_price(cls, v):
    return v.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) 
    class Config:
        orm_mode = True 

class Order(BaseModel):
    id: int
    user_id: Optional[int]
    full_name: str
    email: str
    total_paid: Decimal
    status: str
    created_at: datetime
    items: List[CartItem] = [] 
    
    class Config:
        from_attributes = True
