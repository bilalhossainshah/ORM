import os
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = "ecommerce_db"

class MongoDatabase:
    client: AsyncIOMotorClient = None
    db = None

mongo_db = MongoDatabase()

async def connect_mongo():
    mongo_db.client = AsyncIOMotorClient(MONGO_URL)
    mongo_db.db = mongo_db.client[MONGO_DB_NAME]
    # Verify connection
    try:
        await mongo_db.client.admin.command('ping')
        print("Connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo():
    mongo_db.client.close()
    print("MongoDB connection closed.")

def get_mongo_db(request: Request):
    return request.app.state.mongo_db_client[MONGO_DB_NAME]

