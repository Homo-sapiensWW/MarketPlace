from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate, UserResponse
from fastapi import Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.auth import hash_password, verify_password, create_access_token
from app.models import Users
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register', response_model=UserResponse)
def user_create(user: UserCreate, db: Session = Depends(get_db)) -> Users:
    existing_user = db.query(Users).filter(Users.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already taken')
    hashing_pass = hash_password(user.password)
    new_user = Users(username=user.username, hashed_password=hashing_pass, balance=100.0)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login')
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: Users | None = db.query(Users).filter(Users.username == form_data.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid login or password")
    access_token = create_access_token(data={'sub': user.username})
    return {"access_token": access_token, "token_type": "bearer"}
