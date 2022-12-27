from configs.connection import database
from passlib.context import CryptContext
from datetime import datetime, timedelta
from utils import constant
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth import model
from jwt import PyJWTError
from pydantic import ValidationError

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

pwd_context = CryptContext(schemes=["bcrypt"])

def findExistedUser(username: str):
    query = "select * from users where status='1' and username=:username"
    return database.fetch_one(query, values={"username":username})

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, constant.SECRET_KEY, algorithm=constant.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, constant.SECRET_KEY, algorithms=[constant.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = model.TokenData(username=username)
    except (PyJWTError, ValidationError):
        raise credentials_exception

    user = await findExistedUser(token_data.username);
    if user is None:
        raise credentials_exception

    return model.UserList(**user)

def get_current_active_user(current_user: model.UserList = Depends(get_current_user)):
    if current_user.status == '9':
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user