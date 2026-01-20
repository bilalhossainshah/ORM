from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from database import engine, Base
from mongo_database import connect_mongo, close_mongo, mongo_db 
from app.routers import product, category, cart, user, mongo_router
import app.models 

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="E-commerce Hybrid API",
    description="A complete API with organized routers for Products, Users, and Carts.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Create database tables
print("Creating database tables if they don't exist...")
Base.metadata.create_all(bind=engine)
print("Database tables ensured.")

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

