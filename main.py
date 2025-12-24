from fastapi import FastAPI
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from mongo_database import connect_mongo, close_mongo, mongo_db 
from app.routers import product, category, cart, user, mongo_router

import app.models 
from dotenv import load_dotenv
load_dotenv()


print("Creating database tables if they don't exist...")
Base.metadata.create_all(bind=engine)
print("Database tables ensured.")


app = FastAPI(
    title="E-commerce Hybrid API",
    description="A complete API with organized routers for Products, Users, and Carts.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_mongo()
    app.state.mongo_db_client = mongo_db.client

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo()


app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(category.router,prefix="/catgory", tags=["category"])
app.include_router(mongo_router.router, prefix="/mongo", tags=["mongo_items"]) 


@app.get("/")
def read_root():
    return {"Welcome": "E-commerce API is running."}

