from passlib.context import CryptContext
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Users
from sqlalchemy import select

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ALGORITHM = "HS256"
load_dotenv()


def hash_password(password: str) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)))
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=ALGORITHM)
    return encoded_jwt


security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                     db: AsyncSession = Depends(get_db)) -> Users:
    token = credentials.credentials
    try:
        decode_jwt = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[ALGORITHM])
        username: str = decode_jwt.get('sub')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401)
    res = await db.execute(select(Users).where(Users.username==username))
    user = res.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=401)
    return user
