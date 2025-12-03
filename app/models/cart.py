from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base 

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) 
    full_name = Column(String(50), nullable=False)
    email = Column(String(254), nullable=False)
    total_paid = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    status = Column(String(20), default="Pending") 
    
    items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order(id={self.id}, total_paid={self.total_paid})>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    price = Column(DECIMAL(10, 2), nullable=False) 
    order = relationship("Order", back_populates="items")
    
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(product_id={self.product_id}, quantity={self.quantity})>"
