from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from domains import goods
from domains.goods.schema import GoodCreate, GoodEdit


router = APIRouter(prefix="/good", tags=["goods"])


@router.get('/{article}')
async def get_good(article: str, db: AsyncSession = Depends(get_db)):
    return await goods.crud.get_good(db, article)


@router.post('/create')
async def create_good(good: GoodCreate, db: AsyncSession = Depends(get_db)):
    return await goods.crud.create_good(db, good)


@router.post('/edit')
async def edit_good(good: GoodEdit, db: AsyncSession = Depends(get_db)):
    return await goods.crud.edit_good(db, good)


@router.get('/delete/{article}')
async def delete_good(article: str, db: AsyncSession = Depends(get_db)):
    return await goods.crud.delete_good(db, article)