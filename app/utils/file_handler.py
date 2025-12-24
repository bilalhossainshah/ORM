"""
File upload utilities for handling product images
"""
import os
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from datetime import datetime
import uuid


UPLOAD_DIR = Path("uploads/products")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Create upload directory if it doesn't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def validate_image_file(file: UploadFile) -> bool:
    """Validate image file"""
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds {MAX_FILE_SIZE / 1024 / 1024}MB limit"
        )
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    return True


async def save_product_image(file: UploadFile) -> str:
    """
    Save uploaded product image and return the file path/URL
    
    Args:
        file: UploadFile from FastAPI
        
    Returns:
        Relative path to saved image
    """
    validate_image_file(file)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    file_ext = Path(file.filename).suffix.lower()
    filename = f"{timestamp}_{unique_id}{file_ext}"
    
    file_path = UPLOAD_DIR / filename
    
    try:
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Return relative URL path
        relative_path = f"/uploads/products/{filename}"
        return relative_path
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save image: {str(e)}"
        )
    finally:
        file.file.close()


def delete_product_image(image_path: str) -> bool:
    """Delete product image from storage"""
    try:
        if image_path.startswith("/uploads/products/"):
            image_path = image_path.replace("/uploads/products/", "")
        
        file_path = UPLOAD_DIR / image_path
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting image: {e}")
        return False
