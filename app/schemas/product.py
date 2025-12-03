from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    title: str = Field(..., example="Laptop Model X")
    description: Optional[str] = Field(None, example="A fast, light laptop.")
    price: Decimal = Field(..., gt=0, decimal_places=2, example=999.99)
    brand: Optional[str] = Field(None, example="BrandName")
    image_url: Optional[str] = Field(None, example="http://example.com/images/laptop.jpg")
    in_stock: bool = Field(True, example=True)

class ProductCreate(ProductBase):
    category_id: int = Field(..., example=1)
    pass

class ProductUpdate(ProductBase):
    title: Optional[str] = None
    price: Optional[Decimal] = None
    category_id: Optional[int] = None
    in_stock: Optional[bool] = None

class Product(ProductBase):
    id: int
    category_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
