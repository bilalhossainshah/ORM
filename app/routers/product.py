from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import or_
from app import models, schemas
from app.models.product import Product
from database import get_db
from app.schemas import product as product_schemas
from app.crud import product as product_crud
from app.utils.file_handler import save_product_image
from app.routers.utils import upload_to_s3


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


@router.post("/upload-image/", response_model=product_schemas.Product)
def create_product(form_data: product_schemas.ProductCreateForm = Depends(), db: Session = Depends(get_db),image: UploadFile = File()):
    payload = form_data.to_schema()
    category = db.query(models.Category).get(payload.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")
    
    print("---------------------------",image.filename)
    file_url=upload_to_s3(image)
    print("File uploaded to S3 at URL:", file_url) 


    
    product = models.Product(
        title=payload.name,
        description=payload.description,
        price=payload.price,
        category_id=payload.category_id,
        total_units=payload.total_units,
        product_image=file_url,
        remaining_units=payload.remaining_units if payload.remaining_units is not None else payload.total_units,
        quantity=payload.quantity
    )

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


