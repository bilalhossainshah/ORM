from sqlalchemy.orm import Session
from app.models import cart as models_cart
from app.models import user as models_user
from app.schemas import cart as schemas_cart
from decimal import Decimal
from fastapi import HTTPException, status

def get_order(db: Session, order_id: int):

    return db.query(models_cart.Order).filter(models_cart.Order.id == order_id).first()


def get_pending_order_for_user(db: Session, user_id: int):
    return db.query(models_cart.Order).filter(
        models_cart.Order.user_id == user_id,
        models_cart.Order.status == "Pending"
    ).first()


def create_new_order(db: Session, user_id: int):
    user = db.query(models_user.User).filter(models_user.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found when creating order"
        )


   
    db_order = models_cart.Order(
        user_id=user_id,
        full_name=user.full_name or "Annonymus user",
        email=user.email,
        total_paid=Decimal('0.00'),
        status="Pending"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def add_item_to_order(db: Session, order_id: int, product_id: int, quantity: int, price: Decimal):
    db_item = models_cart.OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        price=price 
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def handle_add_to_cart(
    db: Session, 
    user_id: int, # We now require user_id
    item_details: schemas_cart.CartItemCreate, 
    current_price: Decimal
):
    
    order = get_pending_order_for_user(db, user_id)
    if not order:
        order = create_new_order(db, user_id)
    
    
    db_item = add_item_to_order(
        db=db,
        order_id=order.id,
        product_id=item_details.product_id,
        quantity=item_details.quantity,
        price=current_price
    )
    return db_item


def update_order_status(db: Session, order_id: int, new_status: str):
    db_order = get_order(db, order_id)
    if db_order:
        db_order.status = new_status
        db.commit()
        db.refresh(db_order)
        return db_order
    return None

