from sqlalchemy.orm import Session
from app.models import product as models_product
from app.schemas import product as schemas_product

def get_product(db: Session, product_id: int):
    return db.query(models_product.Product).filter(models_product.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_product.Product).offset(skip).limit(limit).all()

def get_product_by_title(db: Session, title: str):
    return db.query(models_product.Product).filter(models_product.Product.title == title).first()

def create_product(db: Session, product: schemas_product.ProductCreate):
    db_product = models_product.Product(
        title=product.title,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
        brand=product.brand,
        image_url=product.image_url,
        in_stock=product.in_stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, updated_data: schemas_product.ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product:
        update_data_dict = updated_data.dict(exclude_unset=True)
        for key, value in update_data_dict.items():
            setattr(db_product, key, value)
        
        db.commit()
        db.refresh(db_product)
        return db_product
    return None

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
