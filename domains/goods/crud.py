from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .model import Good, GoodComponent
from .schema import GoodCreate, GoodGetFilter, GoodEdit, GoodComponentCreate, GoodComponentEdit, GoodTopup


async def create_good(db: AsyncSession, item: GoodCreate) -> None:
    good = Good(**item.model_dump())
    db.add(good)
    await db.commit()
    await db.refresh(good)


async def get_good(db: AsyncSession, article: int) -> Good | None:
    return await db.get(Good, article)


async def get_goods(db: AsyncSession, filter: GoodGetFilter) -> list[Good]:
    query = select(Good)
    if filter.article:
        query = query.where(Good.article == filter.article)
    if filter.name:
        query = query.where(Good.name == filter.name)
    if filter.current_stock:
        query = query.where(Good.current_stock == filter.current_stock)
    result = await db.execute(query)
    return list(result.scalars().all())


async def edit_good(db: AsyncSession, data: GoodEdit) -> None:
    good = await db.get(Good, data.article)
    if not good:
        raise ValueError(f"Товар с article={data.article} не найден")
    for key, value in data.model_dump(exclude_none=True, exclude={"article"}).items():
        setattr(good, key, value)
    await db.commit()
    await db.refresh(good)


async def delete_good(db: AsyncSession, article: int) -> None:
    good = await db.get(Good, article)
    if not good:
        raise ValueError(f"Товар с article={article} не найден")
    await db.delete(good)
    await db.commit()

async def topup_good(db: AsyncSession, data: GoodTopup) -> Good:
    good = await db.get(Good, data.id)
    if not good:
        raise ValueError(f"Товар с id={data.id} не найден")
    good.current_stock += data.amount
    await db.commit()
    await db.refresh(good)
    return good

#component
async def add_good_component(db: AsyncSession, item: GoodComponentCreate) -> None:
    component = GoodComponent(**item.model_dump())
    db.add(component)
    await db.commit()
    await db.refresh(component)


async def get_good_components(db: AsyncSession, good_article: int) -> list[GoodComponent]:
    query = select(GoodComponent).where(GoodComponent.good_article == good_article)
    result = await db.execute(query)
    return list(result.scalars().all())


async def edit_good_component(db: AsyncSession, data: GoodComponentEdit) -> None:
    component = await db.get(GoodComponent, data.id)
    if not component:
        raise ValueError(f"Компонент с id={data.id} не найден")
    for key, value in data.model_dump(exclude_none=True, exclude={"id"}).items():
        setattr(component, key, value)
    await db.commit()
    await db.refresh(component)


async def delete_good_component(db: AsyncSession, id: int) -> None:
    component = await db.get(GoodComponent, id)
    if not component:
        raise ValueError(f"Компонент с id={id} не найден")
    await db.delete(component)
    await db.commit()