from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from app.utils.auth import get_current_user
from domains import details
from domains.details.schema import DetailCreate, DetailEdit, DetailGetFilter, DetailComponentCreate, DetailComponentEdit

router = APIRouter(prefix="/detail", tags=["details"])


@router.get('/{article}')
async def get_detail(article: int, db: AsyncSession = Depends(get_db),
                     current_user: dict = Depends(get_current_user)):
    return await details.service.get_detail(db, article)


@router.post('/get')
async def get_details(filter: DetailGetFilter, db: AsyncSession = Depends(get_db),
                      current_user: dict = Depends(get_current_user)):
    return await details.service.get_details(db, filter)


@router.post('/create')
async def create_detail(detail: DetailCreate, db: AsyncSession = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    return await details.service.create_detail(db, detail)


@router.post('/edit')
async def edit_detail(detail: DetailEdit, db: AsyncSession = Depends(get_db),
                      current_user: dict = Depends(get_current_user)):
    return await details.service.edit_detail(db, detail)


@router.get('/delete/{article}')
async def delete_detail(article: int, db: AsyncSession = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    return await details.service.delete_detail(db, article)


@router.post('/component/add')
async def add_component(item: DetailComponentCreate, db: AsyncSession = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    return await details.service.add_component(db, item)


@router.get('/component/{parent_article}')
async def get_components(parent_article: int, db: AsyncSession = Depends(get_db),
                         current_user: dict = Depends(get_current_user)):
    return await details.service.get_components(db, parent_article)


@router.post('/component/edit')
async def edit_component(item: DetailComponentEdit, db: AsyncSession = Depends(get_db),
                         current_user: dict = Depends(get_current_user)):
    return await details.service.edit_component(db, item)


@router.get('/component/delete/{id}')
async def delete_component(id: int, db: AsyncSession = Depends(get_db),
                            current_user: dict = Depends(get_current_user)):
    return await details.service.delete_component(db, id)