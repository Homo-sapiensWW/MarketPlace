from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import Users, Item
from app.schemas import CategoryResponse, CategoryCreate, UserResponse, ItemResponse
from app.models import Category
from sqlalchemy import select


def require_admin(current_user: Users = Depends(get_current_user)) -> Users:
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='not enough permissions')
    return current_user


router = APIRouter(prefix='/admin', tags=['Admin'], dependencies=[Depends(require_admin)])


@router.post('/categories', response_model=CategoryResponse)
async def category_create(category: CategoryCreate, db: AsyncSession = Depends(get_db)) -> Category:
    res = await db.execute(select(Category).where(Category.name == category.name))
    if res.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail='category already existing')
    db_category = Category(name=category.name)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


@router.patch('/users/{user_id}/role', response_model=UserResponse)
async def switch_role(user_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Users).where(Users.id==user_id))
    get_user = res.scalar_one_or_none()
    if not get_user:
        raise HTTPException(status_code=404, detail='user not found')
    get_user.role = 'admin'
    await db.commit()
    await db.refresh(get_user)
    return get_user


@router.delete('/items/{item_id}', status_code=204)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Item).where(Item.id==item_id))
    item = res.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail='item not found')
    await db.delete(item)
    await db.commit()
    return {"message": "Item deleted"}
