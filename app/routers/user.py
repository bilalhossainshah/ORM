from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.schemas import user as user_schemas
from app.crud import user as user_crud

router = APIRouter()

@router.post("/register/", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
   
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@router.post("/login/")
def login_user(user_credentials: user_schemas.UserLogin, db: Session = Depends(get_db)):
    
    db_user = user_crud.get_user_by_email(db, email=user_credentials.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not user_crud.verify_password(user_credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
        
    return {"message": "Login successful", "user_id": db_user.id}

@router.get("/{user_id}", response_model=user_schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
  
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
