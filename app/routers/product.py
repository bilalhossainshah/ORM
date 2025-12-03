from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from app.schemas import product as product_schemas
from app.crud import product as product_crud

router = APIRouter()

@router.get("/", response_model=List[product_schemas.Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   
    products = product_crud.get_products(db, skip=skip, limit=limit)
    return products

@router.post("/", response_model=product_schemas.Product, status_code=status.HTTP_201_CREATED)
def create_new_product(product: product_schemas.ProductCreate, db: Session = Depends(get_db)):
    
    db_product = product_crud.get_product_by_title(db, title=product.title)
    if db_product:
        raise HTTPException(status_code=400, detail="Product title already registered")
    return product_crud.create_product(db=db, product=product)

@router.get("/{product_id}", response_model=product_schemas.Product)
def get_product_details(product_id: int, db: Session = Depends(get_db)):
    
    product = product_crud.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=product_schemas.Product)
def update_product_details(
    product_id: int, 
    updated_product: product_schemas.ProductUpdate, 
    db: Session = Depends(get_db)
):
  
    product = product_crud.update_product(db, product_id=product_id, updated_data=updated_product)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
   
    success = product_crud.delete_product(db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"message": "Product deleted successfully"}
