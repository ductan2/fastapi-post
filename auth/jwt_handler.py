from datetime import timedelta, datetime

from decouple import config
from sqlalchemy.orm import Session

import database
import users.user_service as user_service
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from fastapi import Depends,HTTPException

JWT_SECRET = config('JWT_SECRET')
JWT_ALGORITHM = config('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    print("to_encode", to_encode)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_user_by_token(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        print("token", token)
        decode = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(decode)
        username: str = decode.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print("error", e)
        raise HTTPException(status_code=401, detail="Invalid token")
    user = user_service.get_user_by_email_or_username(db, identifier=username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


