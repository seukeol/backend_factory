from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .model import Post
from .schema import PostFilter


async def get_posts(db: AsyncSession, department: str) -> list:
    query = select(Post)
    if department:
        query = query.where(Post.department == department)
    result = await db.execute(query)
    return [[post.id, post.name] for post in result.scalars().all()]


