from sqlalchemy.ext.asyncio import AsyncSession
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpInteger, value

from domains.cutting.crud import get_schemes_for_detail, get_scheme_outputs


async def find_best_cutting_plan(db: AsyncSession, deficit: dict[int, float]) -> dict:
    """
    deficit: {detail_article: нехватка} например {10: 50, 11: 30}
    Возвращает: {scheme_id: сколько раз запустить}
    """

    # Собираем все схемы которые производят хоть одну из нужных деталей
    all_scheme_ids = set()
    for detail_article in deficit:
        schemes = await get_schemes_for_detail(db, detail_article)
        for scheme in schemes:
            all_scheme_ids.add(scheme.id)

    if not all_scheme_ids:
        return {}

    # Для каждой схемы загружаем выходы: {scheme_id: {detail_article: quantity}}
    scheme_outputs = {}
    for scheme_id in all_scheme_ids:
        outputs = await get_scheme_outputs(db, scheme_id)
        scheme_outputs[scheme_id] = {o.detail_article: o.quantity for o in outputs}

    # LP задача
    prob = LpProblem("cutting_plan", LpMinimize)

    # Переменные: сколько раз запустить каждую схему (целое, >= 0)
    x = {
        scheme_id: LpVariable(f"x_{scheme_id}", lowBound=0, cat=LpInteger)
        for scheme_id in all_scheme_ids
    }

    # Ограничения: для каждой детали сумма выхода по всем схемам >= дефицит
    for detail_article, needed in deficit.items():
        prob += lpSum(
            scheme_outputs[scheme_id].get(detail_article, 0) * x[scheme_id]
            for scheme_id in all_scheme_ids
        ) >= needed

    # Минимизируем: суммарный излишек по всем деталям
    prob += lpSum(
        lpSum(
            scheme_outputs[scheme_id].get(detail_article, 0) * x[scheme_id]
            for scheme_id in all_scheme_ids
        ) - needed
        for detail_article, needed in deficit.items()
    )

    print("DEFICIT:", deficit)
    print("SCHEME OUTPUTS:", scheme_outputs)

    prob.solve()
    print("STATUS:", prob.status, value(prob.objective))
    for scheme_id in all_scheme_ids:
        print(f"x_{scheme_id} =", value(x[scheme_id]))

    result = {
        scheme_id: int(value(x[scheme_id]))
        for scheme_id in all_scheme_ids
        if value(x[scheme_id]) and value(x[scheme_id]) > 0
    }

    return result