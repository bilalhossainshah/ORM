from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.schemas.wishlist import WishlistItem
from typing import List
from mongo_database import get_mongo_db # The dependency function
from bson import ObjectId

router = APIRouter()

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict."""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("/", response_model=WishlistItem)
async def create_wishlist_item(request: Request, item: WishlistItem = Body(...)):
    item = jsonable_encoder(item)
    mongo_collection = request.app.state.mongo_db_client["ecommerce_db"]["wishlist"]
    new_item = await mongo_collection.insert_one(item)
    created_item = await mongo_collection.find_one({"_id": new_item.inserted_id})
    return serialize_doc(created_item)

@router.get("/", response_model=List[WishlistItem])
async def list_wishlist_items(request: Request):
    mongo_collection = request.app.state.mongo_db_client["ecommerce_db"]["wishlist"]
    items = []
    cursor = mongo_collection.find({})
    async for doc in cursor:
        items.append(serialize_doc(doc))
    return items
