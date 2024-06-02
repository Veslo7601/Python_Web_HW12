from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from starlette import status

from My_project.database.database import get_database
from My_project.database.models import User


class Hash:
    """Class for hash"""
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        """Function verify password"""
        return self.context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        """Function to get password"""
        return self.context.hash(password)

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def create_access_token(data: dict, expires_delta: Optional[float] = None):
    """Function create access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"iat": datetime.now(), "exp": expire, "scope": "access_token"})
    encode_access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_access_token

async def create_refresh_token( data: dict, expires_delta: Optional[float] = None):
    """Function create refresh token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now() + timedelta(days=7)
    to_encode.update({"iat": datetime.now(), "exp": expire, "scope": "refresh_token"})
    encode_access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_access_token


async def get_email_from_refresh_token(refresh_token: str):
    """function get email"""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload['scope'] == 'refresh_token'
            email = payload['sub']
            return email
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid scope for token")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_database)):
    """function get current user"""
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        if payload['scope']== "access_token":
            email = payload["sub"]
            if email is None:
                raise exception
        else:
            raise exception
    except JWTError as e:
        raise exception
    
    user: User = db.query(User).filter(User.email == email).first()
    if user is None:
        raise exception
    return user

