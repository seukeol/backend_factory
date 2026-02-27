from sqlalchemy.ext.asyncio import AsyncSession
from .model import Good
from domains.goods.schema import GoodEdit
from .schema import GoodCreate

async def create_good(db: AsyncSession, item: GoodCreate) -> None:
    existing = await db.get(Good, item.article)
    if existing:
        raise ValueError(f"Товар с article={item.article} уже существует")
    good = Good(**item.model_dump())
    db.add(good)
    await db.commit()
    await db.refresh(good)

async def get_good(db: AsyncSession, article: str) -> Good | None:
    return await db.get(Good, article)

async def edit_good(db: AsyncSession, data: GoodEdit) -> None:
    good = await db.get(Good, data.article)
    if not good:
        raise ValueError(f"Товар с article={data.article} не найден")
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(good, key, value)
    await db.commit()
    await db.refresh(good)

async def delete_good(db: AsyncSession, article: str) -> None:
    good = await db.get(Good, article)
    if not good:
        raise ValueError(f"Товар с article={article} не найден")
    await db.delete(good)
    await db.commit()