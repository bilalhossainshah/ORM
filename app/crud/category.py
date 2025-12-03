
from sqlalchemy.orm import Session
from app.models import category as models_category
from app.models import product as models_product 
from app.schemas import category as schemas_category
from typing import List

def get_category(db: Session, category_id: int):
    return db.query(models_category.Category).filter(models_category.Category.id == category_id).first()

def get_categories(db: Session):
    return db.query(models_category.Category).all()

def get_category_by_name(db: Session, name: str):
    return db.query(models_category.Category).filter(models_category.Category.name == name).first()

def create_category(db: Session, category: schemas_category.CategoryCreate):
    db_category = models_category.Category(
        name=category.name,
        slug=category.slug or category.name.lower().replace(" ", "-")
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_products_in_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    return db.query(models_product.Product).filter(
        models_product.Product.category_id == category_id
    ).offset(skip).limit(limit).all()

