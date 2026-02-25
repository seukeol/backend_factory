from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base



DATABASE_URL = "sqlite+aiosqlite:///sqlite3.db"
engine = create_async_engine(DATABASE_URL, echo=True)



AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    db = AsyncSession()
    try:
        yield db
    finally:
        await db.close()