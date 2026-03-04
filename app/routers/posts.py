from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from domains import posts, users
from domains.posts.schema import PostFilter
from app.utils.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get('/get_posts')
async def get_posts(current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await users.crud.get_user_from_db_by_id(db, current_user.get("user_id"))
    return await posts.crud.get_posts(db, user.department)