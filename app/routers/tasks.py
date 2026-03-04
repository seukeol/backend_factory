from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from app.utils.auth import get_current_user
from domains import tasks, users
from domains.tasks.schema import TaskCreate, TaskFilter, TaskEdit, TaskTopup

router = APIRouter(prefix="/task", tags=["tasks"])

@router.get('/get')
async def get_tasks(post: str, db: AsyncSession = Depends(get_db),  current_user: dict = Depends(get_current_user)):
    user = await users.crud.get_user_from_db_by_id(db, current_user.get("user_id"))
    filter = TaskFilter(department=user.department, post=post)
    return await tasks.crud.get_tasks(db, filter)

@router.post('/create')
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await tasks.crud.create_task(db, task)

@router.post('/edit')
async def edit_task(task: TaskEdit, db: AsyncSession = Depends(get_db)):
    return await tasks.crud.edit_task(db, task)

@router.post('/topup')
async def topup_task(task: TaskTopup, db: AsyncSession = Depends(get_db)):
    return await tasks.crud.topup_task(db, task)

@router.get('/delete/{id}')
async def delete_task(id: int, db: AsyncSession = Depends(get_db)):
    return await tasks.crud.delete_task(db, id)