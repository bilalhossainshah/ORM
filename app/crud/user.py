from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models import user as models_user
from app.schemas import user as schemas_user
import secrets
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, user_id: int):
    return db.query(models_user.User).filter(models_user.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models_user.User).filter(models_user.User.email == email).first()

def create_user(db: Session, user: schemas_user.UserCreate):
    hashed_password = get_password_hash(user.password)
    verification_token = str(secrets.randbelow(1000000)).zfill(6)  # 6-digit code
    
    db_user = models_user.User(
        email=user.email, 
        full_name=user.full_name, 
        hashed_password=hashed_password,
        is_verified=False,
        verification_token=verification_token
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user, verification_token

def verify_email(db: Session, code: str):
    """Mark email as verified by code"""
    user = db.query(models_user.User).filter(
        models_user.User.verification_token == code
    ).first()
    
    if not user:
        return None
    
    user.is_verified = True
    user.verification_token = None
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, user_update: dict):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    for key, value in user_update.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def create_password_reset_token(db: Session, email: str):
    """Create password reset token for user"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    reset_token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=1)
    
    user.reset_token = reset_token
    user.reset_token_expires = expires
    db.commit()
    db.refresh(user)
    return reset_token

def reset_password(db: Session, token: str, new_password: str):
    """Reset password using token"""
    user = db.query(models_user.User).filter(
        models_user.User.reset_token == token
    ).first()
    
    if not user or user.reset_token_expires < datetime.utcnow():
        return None
    
    user.hashed_password = get_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    db.refresh(user)
    return user
