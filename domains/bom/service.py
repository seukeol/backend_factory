from sqlalchemy.ext.asyncio import AsyncSession

from domains.details.crud import update_availability
from domains.details.service import get_detail, get_parents, get_components


async def _count_availability(db: AsyncSession, detail_article: int):
    minimum = 2**31 - 1
    detail_components = await get_components(db, detail_article)
    for detail_component in detail_components:
        detail_component_info = await get_detail(db, detail_component.child_article)
        print(f"DEBUG detail_component: {detail_component}")
        print(f"DEBUG detail_component_info: {detail_component_info}")
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


async def get_all_components_list(db: AsyncSession, detail_article: int, quantity: float = 1) -> list:
    from domains.cutting.crud import get_schemes_for_detail
    detail_components = await get_components(db, detail_article)
    if not detail_components:
        schemes = await get_schemes_for_detail(db, detail_article)
        if not schemes:
            return []
        scheme = schemes[0]
        scheme_inputs = await get_components(db, -scheme.id)
        result = []
        for inp in scheme_inputs:
            input_detail = await get_detail(db, inp.child_article)
            result.append((input_detail, inp.quantity))
            result += await get_all_components_list(db, inp.child_article, inp.quantity)
        return result

    result = []
    for component in detail_components:
        component_detail = await get_detail(db, component.child_article)
        accumulated_quantity = quantity * component.quantity
        result.append((component_detail, accumulated_quantity))
        result += await get_all_components_list(db, component.child_article, accumulated_quantity)
    return result