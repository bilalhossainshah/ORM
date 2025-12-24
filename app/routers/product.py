from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from app.schemas import product as product_schemas
from app.crud import product as product_crud
from app.utils.file_handler import save_product_image

router = APIRouter()

@router.get("/", response_model=List[product_schemas.Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   
    products = product_crud.get_products(db, skip=skip, limit=limit)
    return products


@router.get("/search/", response_model=List[product_schemas.Product])
def search_products(
    q: str = Query(..., min_length=1, max_length=100),
    db: Session = Depends(get_db)
):
    """
    Search products by title or description
    
    Example: /products/search/?q=jacket
    """
    from sqlalchemy import or_
    from app.models.product import Product
    
    products = db.query(Product).filter(
        or_(
            Product.title.ilike(f"%{q}%"),
            Product.description.ilike(f"%{q}%")
        )
    ).all()
    
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No products found matching '{q}'"
        )
    return products


@router.get("/filter/", response_model=List[product_schemas.Product])
def filter_products(
    category: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    brand: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    Filter products by category, price range, and brand
    
    Example: /products/filter/?category=electronics&min_price=100&max_price=500
    """
    from sqlalchemy import and_
    from app.models.product import Product
    
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))
    
    products = query.all()
    
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found with the given filters"
        )
    return products


@router.post("/upload-image/", response_model=dict)
async def upload_product_image(file: UploadFile = File(...)):
    """
    Upload product image and return the image URL
    
    Returns: {"image_url": "/uploads/products/filename.jpg"}
    """
    image_url = await save_product_image(file)
    return {"image_url": image_url}

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
