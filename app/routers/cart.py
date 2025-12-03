from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.schemas import cart as cart_schemas
from app.crud import cart as cart_crud
from app.crud import product as product_crud 

router = APIRouter()

class AddItemInput(cart_schemas.CartItemCreate):
    user_id: int 

@router.post("/add-item/", response_model=cart_schemas.CartItem)
def add_item_to_cart(
    input_data: AddItemInput, 
    db: Session = Depends(get_db)
):
    
    product = product_crud.get_product(db, product_id=input_data.product_id)
    if not product or not product.in_stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or out of stock")
    
   
    cart_item = cart_crud.handle_add_to_cart(
        db=db, 
        user_id=input_data.user_id,
        item_details=input_data, 
        current_price=product.price
    )
    return cart_item

@router.get("/{order_id}/", response_model=cart_schemas.Order)
def view_cart_details(order_id: int, db: Session = Depends(get_db)):
    order = cart_crud.get_order(db, order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order (Cart) not found" 
        )
    return order





@router.post("/{order_id}/checkout/", response_model=cart_schemas.Order)
def process_checkout(order_id: int, db: Session = Depends(get_db)):
   
    
    updated_order = cart_crud.update_order_status(db, order_id=order_id, new_status="Processing")
    
    if not updated_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Could not process checkout"
        )
        
    
    return updated_order
