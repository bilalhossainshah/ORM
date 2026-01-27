from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.schemas import cart as cart_schemas
from app.schemas.checkout import CheckoutRequest, OrderConfirmation
from app.crud import cart as cart_crud
from app.crud import product as product_crud
from app.dependencies import get_current_user
from app.utils.jwt_utils import TokenData
from datetime import datetime, timedelta 
from app.models.cart import OrderItem

router = APIRouter()

class AddItemInput(cart_schemas.CartItemCreate):
    user_id: int 

@router.post("/add-item/", response_model=cart_schemas.CartItem)
def add_item_to_cart(
    input_data: AddItemInput, 
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    
    if current_user.user_id != input_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only add items to your own cart"
        )
    
    product = product_crud.get_product(db, product_id=input_data.product_id)
    if not product or not product.in_stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or out of stock")
    
   
    orders_item = cart_crud.handle_add_to_cart(
        db=db, 
        user_id=input_data.user_id,
        item_details=input_data, 
        current_price=product.price
    )
    return orders_item


@router.put("/update-item/{item_id}")
def update_cart_item(
    item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    
    from app.models.cart import CartItem
    
    cart_item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    order = cart_crud.get_order(db, order_id=cart_item.order_id)
    if order.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only modify your own cart items"
        )
    
    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0"
        )
    
    product = product_crud.get_product(db, product_id=cart_item.product_id)
    if quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.stock} items available"
        )
    
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    
    return {"message": "Item updated", "item": cart_item}


@router.delete("/remove-item/{item_id}")
def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
   
    
    
    orders_item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
    if not orders_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    order = cart_crud.get_order(db, order_id=orders_item.order_id)
    if order.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only remove items from your own cart"
        )
    
    db.delete(orders_item)
    db.commit()
    
    return {"message": "Item removed from cart"}


@router.get("/{order_id}/", response_model=cart_schemas.Order)
def view_cart_details(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
   
    order = cart_crud.get_order(db, order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order (Cart) not found" 
        )
    
    if order.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own cart"
        )
    
    return order





@router.post("/{order_id}/checkout/", response_model=OrderConfirmation)
def process_checkout(
    order_id: int,
    checkout_data: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    
    order = cart_crud.get_order(db, order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only checkout your own order"
        )
    
    if checkout_data.order_id != order_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order ID mismatch"
        )
    
    
    updated_order = cart_crud.update_order_status(db, order_id=order_id, new_status="Processing")
    
    if not updated_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Could not process checkout"
        )
    
    estimated_delivery = (datetime.utcnow() + timedelta(days=6)).strftime("%Y-%m-%d")
    
    return OrderConfirmation(
        order_id=order_id,
        status="Processing",
        shipping_address=checkout_data.shipping_address,
        estimated_delivery=estimated_delivery,
        tracking_number=f"TRACK-{order_id}-{datetime.utcnow().strftime('%Y%m%d')}"
    )
