from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from fastapi import Depends
app = FastAPI()

from database import Base
from database import engine
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


from domains import goods
from domains.goods.schema import GoodCreate, GoodEdit

@app.get('/good/{article}')
async def get_good(article: str, db: AsyncSession = Depends(get_db)):
    return await goods.crud.get_good(db, article)

@app.post('/good/create')
async def create_good(good: GoodCreate, db: AsyncSession = Depends(get_db)):
    return await goods.crud.create_good(db, good)

@app.post('/good/edit')
async def edit_good(good: GoodEdit, db: AsyncSession = Depends(get_db)):
    return await goods.crud.edit_good(db, good)

@app.get('/good/delete/{article}')
async def delete_good(article: str, db: AsyncSession = Depends(get_db)):
    return await goods.crud.delete_good(db, article)



from domains import users
from domains.users.schema import UserCreate, UserFilter, UserEdit

@app.post('/user/get')
async def get_users(filter: UserFilter, db: AsyncSession = Depends(get_db)):
    return await users.crud.get_users(db, filter)

@app.post('/user/create')
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await users.crud.create_user(db, user)

@app.post('/user/edit')
async def edit_task(user: UserEdit, db: AsyncSession = Depends(get_db)):
    return await users.crud.edit_user(db, user)

@app.get('/user/delete/{id}')
async def delete_task(id: int, db: AsyncSession = Depends(get_db)):
    return await tasks.crud.delete_task(db, id)



from domains import tasks
from domains.tasks.schema import TaskCreate, TaskFilter, TaskEdit

@app.post('/task/get')
async def get_tasks(filter: TaskFilter, db: AsyncSession = Depends(get_db)):
    return await tasks.crud.get_tasks(db, filter)

@app.post('/task/create')
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await tasks.crud.create_task(db, task)

@app.post('/task/edit')
async def edit_task(task: TaskEdit, db: AsyncSession = Depends(get_db)):
    return await tasks.crud.edit_task(db, task)

@app.get('/task/delete/{id}')
async def delete_task(id: int, db: AsyncSession = Depends(get_db)):
    return await tasks.crud.delete_task(db, id)


