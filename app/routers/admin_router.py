from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import Users, Item
from app.schemas import CategoryResponse, CategoryCreate, UserResponse, ItemResponse
from app.models import Category


def require_admin(current_user: Users = Depends(get_current_user)) -> Users:
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='not enough permissions')
    return current_user


router = APIRouter(prefix='/admin', tags=['Admin'], dependencies=Depends(require_admin))


@router.post('/categories', response_model=CategoryResponse)
def category_create(category: CategoryCreate, db: Session = Depends(get_db)) -> Category:
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail='category already existing')
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.patch('/users/{user_id}/role', response_model=UserResponse)
def switch_role(user_id: int, db: Session = Depends(get_db)):
    get_user: Users | None = db.query(Users).filter(Users.id == user_id).first()
    if not get_user:
        raise HTTPException(status_code=404, detail='user not found')
    get_user.role = 'admin'
    db.commit()
    db.refresh(get_user)
    return get_user


@router.delete('/items/{item_id}', response_model=ItemResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item: Item | None = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='item not found')
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}
