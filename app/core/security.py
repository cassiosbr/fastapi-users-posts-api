from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from app.core.config import settings

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.token import decode_token
from app.core.oauth import oauth2_scheme

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    # Adiciona o id do usuário ao token se estiver presente em data
    if "id" in data:
        to_encode["id"] = data["id"]

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    if not token or token.count(".") != 2:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        token_data = decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = token_data.get("id")
    email = token_data.get("email")

    user = db.query(User).filter(User.id == user_id, User.email == email).first()

    if not user or user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user