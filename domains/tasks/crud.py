from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .model import Task
from .schema import TaskCreate, TaskGetFilter, TaskTopup, TaskEdit


async def create_task(db: AsyncSession, item: TaskCreate) -> Task:
    task = Task(**item.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_task(db: AsyncSession, id: int) -> Task | None:
    return await db.get(Task, id)


async def get_tasks(db: AsyncSession, filter: TaskGetFilter) -> list[Task]:
    query = select(Task).where(Task.available == True)
    if filter.order_id:
        query = query.where(Task.order_id == filter.order_id)
    if filter.detail_article:
        query = query.where(Task.detail_article == filter.detail_article)
    if filter.department:
        query = query.where(Task.department == filter.department)
    if filter.post:
        query = query.where(Task.post == filter.post)
    if filter.priority:
        query = query.where(Task.priority == filter.priority)
    if filter.deadline:
        query = query.where(Task.deadline == filter.deadline)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_tasks_for_order(db: AsyncSession, order_id: int) -> list[Task]:
    query = select(Task).where(Task.order_id == order_id)
    result = await db.execute(query)
    return list(result.scalars().all())


async def edit_task(db: AsyncSession, data: TaskEdit) -> None:
    task = await db.get(Task, data.id)
    if not task:
        raise ValueError(f"Задача с id={data.id} не найдена")
    for key, value in data.model_dump(exclude_none=True, exclude={"id"}).items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)


async def topup_task(db: AsyncSession, data: TaskTopup) -> Task:
    task = await db.get(Task, data.id)
    if not task:
        raise ValueError(f"Задача с id={data.id} не найдена")
    task.amount_done += data.amount_done
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, id: int) -> None:
    task = await db.get(Task, id)
    if not task:
        raise ValueError(f"Задача с id={id} не найдена")
    await db.delete(task)
    await db.commit()