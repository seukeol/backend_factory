from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from app.utils.auth import get_current_user
from domains import goods
from domains.goods.schema import GoodCreate, GoodEdit, GoodGetFilter, GoodComponentCreate, GoodComponentEdit

router = APIRouter(prefix="/good", tags=["goods"])


@router.get('/{article}')
async def get_good(article: int, db: AsyncSession = Depends(get_db),
                   current_user: dict = Depends(get_current_user)):
    return await goods.service.get_good(db, article)


@router.post('/get')
async def get_goods(filter: GoodGetFilter, db: AsyncSession = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    return await goods.service.get_goods(db, filter)


@router.post('/create')
async def create_good(good: GoodCreate, db: AsyncSession = Depends(get_db),
                      current_user: dict = Depends(get_current_user)):
    return await goods.service.create_good(db, good)


@router.post('/edit')
async def edit_good(good: GoodEdit, db: AsyncSession = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    return await goods.service.edit_good(db, good)


@router.get('/delete/{article}')
async def delete_good(article: int, db: AsyncSession = Depends(get_db),
                      current_user: dict = Depends(get_current_user)):
    return await goods.service.delete_good(db, article)


@router.post('/component/add')
async def add_component(item: GoodComponentCreate, db: AsyncSession = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    return await goods.service.add_good_component(db, item)


@router.get('/component/{good_article}')
async def get_components(good_article: int, db: AsyncSession = Depends(get_db),
                         current_user: dict = Depends(get_current_user)):
    return await goods.service.get_good_components(db, good_article)


@router.post('/component/edit')
async def edit_component(item: GoodComponentEdit, db: AsyncSession = Depends(get_db),
                         current_user: dict = Depends(get_current_user)):
    return await goods.service.edit_good_component(db, item)


@router.get('/component/delete/{id}')
async def delete_component(id: int, db: AsyncSession = Depends(get_db),
                            current_user: dict = Depends(get_current_user)):
    return await goods.service.delete_good_component(db, id)