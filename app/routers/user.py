from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.schemas import user as user_schemas
from app.crud import user as user_crud
from app.utils.jwt_utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.email_utils import send_verification_email, send_password_reset_email
from datetime import timedelta
import asyncio
from fastapi import BackgroundTasks
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/register/", status_code=status.HTTP_201_CREATED)
def register_user(
    user: user_schemas.UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user, verification_token = user_crud.create_user(db=db, user=user)

    background_tasks.add_task(
        send_verification_email,
        user.email,
        verification_token
    )

    return {
        "id": db_user.id,
        "email": db_user.email,
        "full_name": db_user.full_name,
        "is_verified": db_user.is_verified,
        "created_at": db_user.created_at,
        "message": "Registration successful! Check your email for verification code."
    }


@router.post("/verify-email/", response_model=user_schemas.User)
def verify_email(request: user_schemas.EmailVerificationRequest, db: Session = Depends(get_db)):
    
    print(f"Verification request received: code={request.code}")
    user = user_crud.verify_email(db, code=request.code)
    if not user:
        print(f"Invalid code: {request.code}")
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
    
    return user

@router.post("/login/")
def login_user(user_credentials: user_schemas.UserLogin, db: Session = Depends(get_db)):
    
    db_user = user_crud.get_user_by_email(db, email=user_credentials.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not db_user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email before logging in"
    )

    
    if not user_crud.verify_password(user_credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": db_user.id, "email": db_user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "email": db_user.email,
        "is_verified": db_user.is_verified
    }

@router.get("/{user_id}", response_model=user_schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
  
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
