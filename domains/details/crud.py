from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from .model import Detail
from .schema import DetailCreate, DetailGetFilter, DetailEdit, DetailTopup
from ..bom.service import recount_availability


async def create_detail(db: AsyncSession, item: DetailCreate) -> None:
    detail = Detail(**item.model_dump())
    db.add(detail)
    await db.commit()
    await db.refresh(detail)


async def get_detail(db: AsyncSession, article: int) -> Detail | None:
    return await db.get(Detail, article)

async def reset_stocks(db: AsyncSession) -> None:
    query = update(Detail).values(stock=0)
    await db.execute(query)
    await db.commit()


async def get_details(db: AsyncSession, filter: DetailGetFilter) -> list[Detail]:
    query = select(Detail)
    if filter.article:
        query = query.where(Detail.article == filter.article)
    if filter.name:
        query = query.where(Detail.name == filter.name)
    if filter.post:
        query = query.where(Detail.post == filter.post)
    result = await db.execute(query)
    return list(result.scalars().all())


async def edit_detail(db: AsyncSession, data: DetailEdit) -> None:
    detail = await db.get(Detail, data.article)
    if not detail:
        raise ValueError(f"Деталь с article={data.article} не найдена")
    for key, value in data.model_dump(exclude_none=True, exclude={"article"}).items():
        setattr(detail, key, value)
    await db.commit()
    await db.refresh(detail)


async def delete_detail(db: AsyncSession, article: int) -> None:
    detail = await db.get(Detail, article)
    if not detail:
        raise ValueError(f"Деталь с article={article} не найдена")
    await db.delete(detail)
    await db.commit()


async def topup_detail(db: AsyncSession, data: DetailTopup) -> Detail:
    detail = await db.get(Detail, data.article)
    if not detail:
        raise ValueError(f"Деталь с article={data.article} не найдена")
    detail.stock += data.amount
    await db.commit()
    await db.refresh(detail)
    return detail


async def topdown_detail(db: AsyncSession, data: DetailTopup) -> Detail:
    detail = await db.get(Detail, data.article)
    if not detail:
        raise ValueError(f"Деталь с article={data.article} не найдена")
    detail.stock -= data.amount
    await db.commit()
    await db.refresh(detail)
    return detail


async def update_availability(db: AsyncSession, article: int, availability: int):
    detail = await db.get(Detail, article)
    if not detail:
        raise ValueError(f"Деталь с article={article} не найдена")
    detail.availability = availability
    await db.commit()
    await db.refresh(detail)


#component
from .model import DetailComponent
from .schema import DetailComponentCreate, DetailComponentEdit

async def add_component(db: AsyncSession, item: DetailComponentCreate) -> None:
    component = DetailComponent(**item.model_dump())
    db.add(component)
    await db.commit()
    await db.refresh(component)


async def get_components(db: AsyncSession, parent_article: int) -> list[DetailComponent]:
    """Что нужно чтобы сделать деталь"""
    query = select(DetailComponent).where(DetailComponent.parent_article == parent_article)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_detail_posts(db: AsyncSession, article: int) -> list:
    detail = await db.get(Detail, article)
    if not detail:
        raise
    return [detail.post, detail.post_alt]

async def get_parents(db: AsyncSession, child_article: int) -> list[DetailComponent]:
    """В каких деталях используется эта деталь"""
    query = select(DetailComponent).where(DetailComponent.child_article == child_article)
    result = await db.execute(query)
    return list(result.scalars().all())


async def edit_component(db: AsyncSession, data: DetailComponentEdit) -> None:
    component = await db.get(DetailComponent, data.id)
    if not component:
        raise ValueError(f"Связь с id={data.id} не найдена")
    component.quantity = data.quantity
    await db.commit()
    await db.refresh(component)


async def delete_component(db: AsyncSession, id: int) -> None:
    component = await db.get(DetailComponent, id)
    if not component:
        raise ValueError(f"Связь с id={id} не найдена")
    await db.delete(component)
    await db.commit()