from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from fastapi import Form

class ProductBase(BaseModel):
    name: str = Field(..., example="Laptop Model X")
    description: Optional[str] = Field(None, example="A fast, light laptop.")
    price: Decimal = Field(..., gt=0, decimal_places=2, example=999.99)
    brand: Optional[str] = Field(None, example="BrandName")
    image_url: Optional[str] = Field(None, example="http://example.com/images/laptop.jpg")
    in_stock: bool = Field(True, example=True)

class ProductCreate(ProductBase):
    name: str = Field(..., example="Laptop Model X")
    description: Optional[str] = Field(None, example="A fast, light laptop.")
    price: Decimal = Field(..., gt=0, decimal_places=2, example=999.99)

    category_id: int = Field(..., example=1)

    total_units: int = Field(..., ge=0, example=100)
    remaining_units: Optional[int] = Field(None, ge=0, example=100)
    quantity: int = Field(..., ge=0, example=10)

    product_image: Optional[str] = Field(None, example="http://example.com/image.jpg")
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
class ProductCreateForm:
    def __init__(
        self,
        title: str = Form(...),
        description: Optional[str] = Form(None),
        price: float = Form(...),
        category_id: int = Form(...),
        total_units: int = Form(...),
        remaining_units: Optional[int] = Form(None),
        quantity: int = Form(...),
        
    ):
        self.name = title
        self.description = description
        self.price = price
        self.category_id = category_id
        self.total_units = total_units
        self.remaining_units = remaining_units
        self.quantity = quantity

    def to_schema(self) -> ProductCreate:
     return ProductCreate(
        title=self.name,
        description=self.description,
        price=self.price,
        category_id=self.category_id,
        total_units=self.total_units,
        quantity=self.quantity,
        remaining_units=self.remaining_units,
    )
