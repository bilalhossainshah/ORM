
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = "yb754f8a036326908537cf0a06f037fd2d6ccfe1a68484a3f1efedd43f328f4f9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    user_id: int
    email: str


class TokenResponse(BaseModel):
    """Response schema for login endpoint"""
    access_token: str
    token_type: str
    user_id: int
    email: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


from jose import JWTError, jwt

def verify_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id = payload.get("user_id")
        email = payload.get("email")

        if user_id is None or email is None:
            return None

        return TokenData(user_id=user_id, email=email)

    except JWTError:
        return None

