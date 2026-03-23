from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from app.utils.auth import get_current_user
from domains import orders
from domains.orders.schema import OrderCreate, OrderEdit, OrderGetFilter

router = APIRouter(prefix="/order", tags=["orders"])


@router.post('/create')
async def create_order(item: OrderCreate, db: AsyncSession = Depends(get_db),
                       current_user: dict = Depends(get_current_user)):
    return await orders.service.create_order(db, item)


@router.post('/get')
async def get_orders(filter: OrderGetFilter, db: AsyncSession = Depends(get_db),
                     current_user: dict = Depends(get_current_user)):
    return await orders.service.get_orders(db, filter)


@router.get('/get/{id}')
async def get_order(id: int, db: AsyncSession = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    return await orders.service.get_order(db, id)


@router.post('/edit')
async def edit_order(item: OrderEdit, db: AsyncSession = Depends(get_db),
                     current_user: dict = Depends(get_current_user)):
    return await orders.service.edit_order(db, item)


@router.get('/delete/{id}')
async def delete_order(id: int, db: AsyncSession = Depends(get_db),
                       current_user: dict = Depends(get_current_user)):
    return await orders.service.delete_order(db, id)