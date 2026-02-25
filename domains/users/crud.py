from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .model import User
from .schema import UserCreate, UserFilter, UserEdit

async def create_user(db: AsyncSession, item: UserCreate) -> None:
    user = User(**item.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)

async def get_users(db: AsyncSession, filter: UserFilter) -> list[User]:
    query = select(User)
    if filter.id:
        query = query.where(User.id == filter.id)
    if filter.name:
        query = query.where(User.name == filter.name)
    if filter.login:
        query = query.where(User.login == filter.login)
    if filter.section_id:
        query = query.where(User.section_id == filter.section_id)
    if filter.group_name:
        query = query.where(User.group_name == filter.group_name)
    result = await db.execute(query)
    return list(result.scalars().all())

async def edit_user(db: AsyncSession, data: UserEdit) -> None:
    user = await db.get(User, data.id)
    if not user:
        raise ValueError(f"Пользователя с id={data.id} не найден")
    for key, value in data.model_dump().items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)

async def delete_user(db: AsyncSession, id: int) -> None:
    user = await db.get(User, id)
    if not user:
        raise ValueError(f"Пользователь с id={id} не найден")
    await db.delete(user)
    await db.commit()