
from fastapi import FastAPI
from database import engine, Base
from app.routers import product, category, cart, user
import app.models 


print("Creating database tables if they don't exist...")
Base.metadata.create_all(bind=engine)
print("Database tables ensured.")


app = FastAPI(
    title="E-commerce API",
    description="A complete API with organized routers for Products, Users, and Carts.",
    version="1.0.0",
)


app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(category.router,prefix="/catgory", tags=["category"])

@app.get("/")
def read_root():
    return {"Welcome": "E-commerce API is running."}

