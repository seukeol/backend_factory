from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .model import Order, OrderStatus
from .schema import OrderCreate, OrderEdit, OrderGetFilter, OrderTopup
from domains import goods
from ..goods.schema import GoodTopup


async def create_order(db: AsyncSession, item: OrderCreate) -> Order:
    order = await crud.create_order(db, item)
    return order


async def get_order(db: AsyncSession, id: int) -> Order | None:
    return await crud.get_order(db, id)


async def get_orders(db: AsyncSession, filter: OrderGetFilter) -> list[Order]:
    return await crud.get_orders(db, filter)


async def edit_order(db: AsyncSession, data: OrderEdit) -> None:
    await crud.edit_order(db, data)


async def delete_order(db: AsyncSession, id: int) -> None:
    await crud.delete_order(db, id)


async def topup_order(db: AsyncSession, data: OrderTopup) -> Order:
    order = await crud.topup_order(db, data)
    if order.amount_done >= order.quantity:
        order.status = OrderStatus.DONE
    good_topup_data = GoodTopup(article=order.good_article, amount=data.amount_done)
    await goods.service.topup_good(db, good_topup_data)
    return order