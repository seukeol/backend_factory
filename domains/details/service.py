from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .schema import DetailCreate, DetailGetFilter, DetailEdit, DetailComponentCreate, DetailComponentEdit, DetailTopup


async def create_detail(db: AsyncSession, item: DetailCreate) -> None:
    await crud.create_detail(db, item)


async def get_detail(db: AsyncSession, article: int):
    return await crud.get_detail(db, article)


async def get_details(db: AsyncSession, filter: DetailGetFilter):
    return await crud.get_details(db, filter)


async def edit_detail(db: AsyncSession, data: DetailEdit) -> None:
    await crud.edit_detail(db, data)


async def delete_detail(db: AsyncSession, article: int) -> None:
    await crud.delete_detail(db, article)


async def topup_detail(db: AsyncSession, filter: DetailTopup):
    await crud.topup_detail(db, filter)


async def topdown_detail(db: AsyncSession, filter: DetailTopup):
    await crud.topdown_detail(db, filter)


async def update_availability(db: AsyncSession, article: int, availability: int):
    await crud.update_availability(db, article, availability)

async def add_component(db: AsyncSession, item: DetailComponentCreate) -> None:
    await crud.add_component(db, item)


async def get_components(db: AsyncSession, parent_article: int):
    return await crud.get_components(db, parent_article)


async def get_detail_posts(db: AsyncSession, detail_article: int):
    return await crud.get_detail_posts(db, detail_article)

async def get_parents(db: AsyncSession, child_article: int):
    return await crud.get_parents(db, child_article)


async def edit_component(db: AsyncSession, data: DetailComponentEdit) -> None:
    await crud.edit_component(db, data)


async def delete_component(db: AsyncSession, id: int) -> None:
    await crud.delete_component(db, id)