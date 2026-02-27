from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domains.tasks.schema import TaskEdit
from .model import Task
from .schema import TaskCreate, TaskFilter, TaskTopup

async def create_task(db: AsyncSession, item: TaskCreate) -> None:
    task = Task(**item.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)

async def get_tasks(db: AsyncSession, filter: TaskFilter) -> list[Task]:
    query = select(Task)
    if filter.id:
        query = query.where(Task.id == filter.id)
    if filter.good_article:
        query = query.where(Task.good_article == filter.good_article)
    if filter.section_id:
        query = query.where(Task.section_id == filter.section_id)
    if filter.group_name:
        query = query.where(Task.group_name == filter.group_name)
    if filter.deadline:
        query = query.where(Task.deadline == filter.deadline)
    result = await db.execute(query)
    return list(result.scalars().all())

async def edit_task(db: AsyncSession, data: TaskEdit) -> None:
    task = await db.get(Task, data.id)
    if not task:
        raise ValueError(f"Задачи с id={data.id} не найден")
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)


async def topup_task(db: AsyncSession, data: TaskTopup) -> None:
    task = await db.get(Task, data.id)
    if not task:
        raise ValueError(f"Задачи с id={data.id} не найден")
    setattr(task, "amount_done", task.amount_done + data.amount_done)
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, id: int) -> None:
    task = await db.get(Task, id)
    if not task:
        raise ValueError(f"Задача с id={id} не найден")
    await db.delete(task)
    await db.commit()