from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserCreate, UserResponse
from fastapi import Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.models import Users
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register', response_model=UserResponse)
async def user_create(user: UserCreate, db: AsyncSession = Depends(get_db)) -> Users:
    res  = await db.execute(select(Users).where(Users.username == user.username))
    existing_user = res.scalar_one_or_none()
    if existing_user is not None:
        raise HTTPException(status_code=400, detail='Username already taken')
    hashing_pass = hash_password(user.password)
    new_user = Users(username=user.username, hashed_password=hashing_pass, balance=100.0)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post('/login')
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Users).where((Users.username == form_data.username)))
    user = res.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid login or password")
    access_token = create_access_token(data={'sub': user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/me', response_model=UserResponse)
async def read_me(current_user = Depends(get_current_user)):
    return current_user