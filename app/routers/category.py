from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from app.schemas import category as category_schemas
from app.crud import category as category_crud
from app.schemas import product as product_schemas 
router = APIRouter()

@router.get("/", response_model=List[category_schemas.Category])
def list_categories(db: Session = Depends(get_db)):
   
    categories = category_crud.get_categories(db)
    return categories

@router.post("/", response_model=category_schemas.Category, status_code=status.HTTP_201_CREATED)
def create_new_category(category: category_schemas.CategoryCreate, db: Session = Depends(get_db)):
   
    db_category = category_crud.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Category name already registered")
    return category_crud.create_category(db=db, category=category)

@router.get("/{category_id}", response_model=category_schemas.Category)
def get_category_details(category_id: int, db: Session = Depends(get_db)):
   
    category = category_crud.get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

@router.get("/{category_id}/products/", response_model=List[product_schemas.Product])
def list_products_by_category(category_id: int, db: Session = Depends(get_db)):
    
    products = category_crud.get_products_in_category(db, category_id=category_id)
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category or products not found")
    return products
