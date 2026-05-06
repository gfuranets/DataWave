from jose import jwt, JWTError
from fastapi import HTTPException
from models import User
from sqlalchemy.orm import Session
from auth import SECRET_KEY, ALGORITHM

def get_user_from_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        return None

    return db.query(User).filter(User.user_id == user_id).first()
