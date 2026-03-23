from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from app.utils.auth import get_current_user
from domains import tasks, users
from domains.tasks.schema import TaskGetFilter, TaskEdit, TaskTopup, TaskPotentialOrder

router = APIRouter(prefix="/task", tags=["tasks"])


@router.post('/get')
async def get_tasks(filter: TaskGetFilter, db: AsyncSession = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    user = await users.crud.get_user_from_db_by_id(db, current_user.get("user_id"))
    if user:
        filter.department = user.department
    return await tasks.service.get_tasks(db, filter)


@router.get('/order/{order_id}')
async def get_tasks_for_order(order_id: int, db: AsyncSession = Depends(get_db),
                               current_user: dict = Depends(get_current_user)):
    return await tasks.service.get_tasks_for_order(db, order_id)


@router.post('/get_potential_tasks')
async def get_potential_tasks(data: TaskPotentialOrder, db: AsyncSession = Depends(get_db)):
    return await tasks.service.get_potential_order_tasks(db, data)


@router.post('/edit')
async def edit_task(task: TaskEdit, db: AsyncSession = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    return await tasks.service.edit_task(db, task)


@router.post('/topup')
async def topup_task(task: TaskTopup, db: AsyncSession = Depends(get_db),
                     current_user: dict = Depends(get_current_user)):
    return await tasks.service.topup_task(db, task)


@router.get('/delete/{id}')
async def delete_task(id: int, db: AsyncSession = Depends(get_db),
                      current_user: dict = Depends(get_current_user)):
    return await tasks.service.delete_task(db, id)