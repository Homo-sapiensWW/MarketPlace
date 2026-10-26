from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Item, Users, Transactions
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.auth import get_current_user
from app.schemas import ItemResponse, ItemCreate, TransactionResponse

router = APIRouter(prefix="/items", tags=["Items"])


@router.get('', response_model=list[ItemResponse])
async def get_items_in_stock(db: AsyncSession = Depends(get_db)) -> list[Item]:
    res = await db.execute(select(Item).where(Item.is_sold==False))
    items_in_stock = res.scalars().all()
    return items_in_stock


@router.post('', response_model=ItemResponse)
async def set_item_on_market(item: ItemCreate, db: AsyncSession = Depends(get_db),
                       current_user: Users = Depends(get_current_user)) -> Item:
    db_item = Item(title=item.title, description=item.description, price=item.price, is_sold=False,
                   category_id=item.category_id, owner_id=current_user.id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.post('/{item_id}/buy', response_model=TransactionResponse)
async def buy_item(item_id: int, db: AsyncSession = Depends(get_db),
             current_user: Users = Depends(get_current_user)) -> Transactions:
    res = await db.execute(select(Item).where((Item.id == item_id)))
    item = res.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail='item not found')
    if item.is_sold:
        raise HTTPException(status_code=400, detail='item was sell')
    if current_user.balance < item.price:
        raise HTTPException(status_code=400, detail='insufficient funds')
    if item.owner_id == current_user.id:
        raise HTTPException(status_code=400, detail='you cant buy yours item')
    current_user.balance -= item.price
    result = await db.execute(select(Users).where((item.owner_id == Users.id)))
    owner = result.scalar_one_or_none()
    if owner is None:
        raise HTTPException(status_code=404)
    owner.balance += item.price
    item.is_sold = True
    item.buyer_id = current_user.id
    db_transaction = Transactions(item_id=item.id, seller_id=item.owner_id, buyer_id=current_user.id, price=item.price)
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction
