from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from domains.cutting.model import CuttingScheme, CuttingSchemeOutput


async def get_schemes_by_post(db: AsyncSession, post: int) -> list[CuttingScheme]:
    result = await db.execute(
        select(CuttingScheme).where(CuttingScheme.post == post)
    )
    return result.scalars().all()


async def get_scheme_outputs(db: AsyncSession, scheme_id: int) -> list[CuttingSchemeOutput]:
    result = await db.execute(
        select(CuttingSchemeOutput).where(CuttingSchemeOutput.scheme_id == scheme_id)
    )
    return result.scalars().all()


async def get_schemes_for_detail(db: AsyncSession, detail_article: int) -> list[CuttingScheme]:
    """Все схемы, которые производят указанную деталь."""
    scheme_ids_query = await db.execute(
        select(CuttingSchemeOutput.scheme_id).where(
            CuttingSchemeOutput.detail_article == detail_article
        )
    )
    scheme_ids = scheme_ids_query.scalars().all()
    if not scheme_ids:
        return []
    result = await db.execute(
        select(CuttingScheme).where(CuttingScheme.id.in_(scheme_ids))
    )
    return result.scalars().all()


async def get_scheme_by_id(db: AsyncSession, scheme_id: int) -> CuttingScheme | None:
    result = await db.execute(
        select(CuttingScheme).where(CuttingScheme.id == scheme_id)
    )
    return result.scalar_one_or_none()