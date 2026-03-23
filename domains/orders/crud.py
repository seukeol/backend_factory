from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .model import Order
from .schema import OrderCreate, OrderEdit, OrderGetFilter, OrderTopup


async def create_order(db: AsyncSession, item: OrderCreate) -> Order:
    order = Order(**item.model_dump())
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def get_order(db: AsyncSession, id: int) -> Order | None:
    return await db.get(Order, id)


async def get_orders(db: AsyncSession, filter: OrderGetFilter) -> list[Order]:
    query = select(Order)
    if filter.good_article:
        query = query.where(Order.good_article == filter.good_article)
    if filter.status:
        query = query.where(Order.status == filter.status)
    result = await db.execute(query)
    return list(result.scalars().all())


async def edit_order(db: AsyncSession, data: OrderEdit) -> None:
    order = await db.get(Order, data.id)
    if not order:
        raise ValueError(f"Заказ с id={data.id} не найден")
    for key, value in data.model_dump(exclude_none=True, exclude={"id"}).items():
        setattr(order, key, value)
    await db.commit()
    await db.refresh(order)


async def delete_order(db: AsyncSession, id: int) -> None:
    order = await db.get(Order, id)
    if not order:
        raise ValueError(f"Заказ с id={id} не найден")
    await db.delete(order)
    await db.commit()


async def topup_order(db: AsyncSession, data: OrderTopup) -> Order:
    order = await db.get(Order, data.id)
    if not order:
        raise ValueError(f"Задача с id={data.id} не найдена")
    order.amount_done += data.amount_done
    await db.commit()
    await db.refresh(order)
    return order