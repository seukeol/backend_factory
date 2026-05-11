from sqlalchemy.ext.asyncio import AsyncSession

from domains.details.crud import update_availability
from domains.details.service import get_detail, get_parents, get_components


async def _count_availability(db: AsyncSession, detail_article: int):
    minimum = 2**31 - 1
    detail_components = await get_components(db, detail_article)
    for detail_component in detail_components:
        detail_component_info = await get_detail(db, detail_component.child_article)
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
    import math
    from domains.cutting.crud import get_schemes_for_detail, get_scheme_outputs
    detail_components = await get_components(db, detail_article)
    if not detail_components:
        schemes = await get_schemes_for_detail(db, detail_article)
        if not schemes:
            return []
        scheme = schemes[0]
        outputs = await get_scheme_outputs(db, scheme.id)
        output_qty = next((o.quantity for o in outputs if o.detail_article == detail_article), 1)
        runs = math.ceil(quantity / output_qty)

        scheme_inputs = await get_components(db, -scheme.id)
        result = []
        for inp in scheme_inputs:
            input_detail = await get_detail(db, inp.child_article)
            input_qty = inp.quantity * runs
            result.append((input_detail, input_qty))
            result += await get_all_components_list(db, inp.child_article, input_qty)
        return result

    result = []
    for component in detail_components:
        component_detail = await get_detail(db, component.child_article)
        accumulated_quantity = quantity * component.quantity
        result.append((component_detail, accumulated_quantity))
        result += await get_all_components_list(db, component.child_article, accumulated_quantity)
    return result