from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Item, Users, Transactions, Category
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.auth import get_current_user
from app.schemas import ItemResponse, ItemCreate, TransactionResponse, CategoryResponse

router = APIRouter(prefix='/category', tags=['Category'])

@router.get('', response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Category))
    categories = res.scalars().all()
    return categories