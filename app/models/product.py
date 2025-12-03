from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base 

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id")) 
    title = Column(String(255), index=True, nullable=False)
    brand = Column(String(255))
    description = Column(String, default="")
    price = Column(DECIMAL(10, 2), nullable=False) 
    image_url = Column(String) 
    in_stock = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


    category = relationship("Category", back_populates="products")

    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product(title='{self.title}', price={self.price})>"
