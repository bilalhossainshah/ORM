from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
import pydantic

try:
    pv_major = int(pydantic.__version__.split('.')[0])
except Exception:
    pv_major = 1


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid objectid")
            return ObjectId(v)
        # Let Pydantic handle other types (e.g., None) or raise
        raise ValueError("Invalid objectid type")

    if pv_major >= 2:
        @classmethod
        def __get_pydantic_json_schema__(cls, core_schema, handler):
            return {"type": "string"}
    else:
        @classmethod
        def __modify_schema__(cls, field_schema):
            # Pydantic v1 JSON schema hook
            field_schema.update(type="string")


class WishlistItem(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id_sqlite: int  # Reference the SQLite user ID
    product_name: str
    priority: int = 1

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
