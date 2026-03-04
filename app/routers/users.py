from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from app.utils.auth import create_access_token
from domains import users
from domains.users.schema import UserCreate, UserFilter, UserEdit, UserLogin

router = APIRouter(prefix="/user", tags=["users"])

@router.post('/get')
async def get_users(filter: UserFilter, db: AsyncSession = Depends(get_db)):
    return await users.crud.get_users(db, filter)

@router.post('/create')
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await users.crud.create_user(db, user)

@router.post('/login')
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await users.crud.get_user_from_db(db, user.login)
    if not db_user:
        return {"error": "Invalid credentials"}
    token = create_access_token({"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.post('/edit')
async def edit_user(user: UserEdit, db: AsyncSession = Depends(get_db)):
    return await users.crud.edit_user(db, user)

@router.get('/delete/{id}')
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    return await users.crud.delete_user(db, id)