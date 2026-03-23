from sqlalchemy.ext.asyncio import AsyncSession

from domains.details.crud import update_availability
from domains.details.service import get_detail, get_parents, get_components


async def _count_availability(db: AsyncSession, detail_article: int):
    minimum = 2**31 - 1
    detail_components = await get_components(db, detail_article)
    for detail_component in detail_components:
        detail_component_info = await get_detail(db, detail_component)
        minimum = min(minimum, detail_component_info.stock / detail_component.quantity)
    return minimum


async def _recount_parents(db: AsyncSession, detail_article: int) -> None:
    """Пересчитывает доступность всех родителей указанной детали."""
    parents = await get_parents(db, detail_article)
    for parent in parents:
        availability = await _count_availability(db, parent.parent_article)
        await update_availability(db, parent.parent_article, availability)


async def recount_availability(db: AsyncSession, detail_article: int) -> None:
    """Пересчитывает родителей поступившей детали и родителей её компонентов."""
    await _recount_parents(db, detail_article)

    components = await get_components(db, detail_article)
    for component in components:
        await _recount_parents(db, component.child_article)


async def get_all_parents_list(db: AsyncSession, detail_article: int, quantity: float = 1) -> list:
    detail_parents = await get_parents(db, detail_article)
    if not detail_parents:
        return []
    result = []
    for parent in detail_parents:
        parent_detail = await get_detail(db, parent.parent_article)
        accumulated_quantity = quantity * parent_detail.quantity
        result.append((parent_detail, accumulated_quantity))
        result += await get_all_parents_list(db, parent.parent_article, accumulated_quantity)
    return result

