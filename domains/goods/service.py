from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .schema import GoodCreate, GoodGetFilter, GoodEdit, GoodComponentCreate, GoodComponentEdit, GoodTopup



async def create_good(db: AsyncSession, item: GoodCreate) -> None:
    await crud.create_good(db, item)


async def get_good(db: AsyncSession, article: int):
    return await crud.get_good(db, article)


async def get_goods(db: AsyncSession, filter: GoodGetFilter):
    return await crud.get_goods(db, filter)


async def edit_good(db: AsyncSession, data: GoodEdit) -> None:
    await crud.edit_good(db, data)


async def delete_good(db: AsyncSession, article: int) -> None:
    await crud.delete_good(db, article)


async def topup_good(db: AsyncSession, filter: GoodTopup):
    await crud.topup_good(db, filter)

async def add_good_component(db: AsyncSession, item: GoodComponentCreate) -> None:
    await crud.add_good_component(db, item)


async def get_good_components(db: AsyncSession, good_article: int):
    return await crud.get_good_components(db, good_article)


async def edit_good_component(db: AsyncSession, data: GoodComponentEdit) -> None:
    await crud.edit_good_component(db, data)


async def delete_good_component(db: AsyncSession, id: int) -> None:
    await crud.delete_good_component(db, id)


async def get_good_with_details(db: AsyncSession, good_article: int):
    return await get_good_bom(db, good_article)
