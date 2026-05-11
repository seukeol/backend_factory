from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .model import Task
from .schema import TaskEdit, TaskGetFilter, TaskTopup, TaskCreate
from domains.orders.service import topup_order
from domains.orders.schema import OrderTopup
from domains.details.schema import DetailTopup
from domains.details.service import topup_detail, get_detail, get_detail_posts, update_availability, get_components
from domains.bom.service import recount_availability, get_all_components_list, _count_availability
from ..details.crud import topdown_detail
from ..goods.service import get_good_components
from domains.posts.crud import get_posts

async def get_task(db: AsyncSession, id: int) -> Task | None:
    return await crud.get_task(db, id)


async def create_task(db: AsyncSession, data: TaskCreate) -> Task:
    await recount_availability(db, data.detail_article)
    return await crud.create_task(db, data)


async def get_tasks(db: AsyncSession, filter: TaskGetFilter, is_admin: bool = False) -> list[Task]:
    return await crud.get_tasks(db, filter, is_admin)


async def get_tasks_for_order(db: AsyncSession, order_id: int) -> list[Task]:
    return await crud.get_tasks_for_order(db, order_id)


async def edit_task(db: AsyncSession, data: TaskEdit) -> None:
    await crud.edit_task(db, data)


async def topup_task(db: AsyncSession, data: TaskTopup) -> Task:
    task = await crud.topup_task(db, data)

    if task.amount_done >= task.amount_needed:
        task.result = True

    if task.detail_article < 0:
        scheme_id = -task.detail_article
        from domains.cutting.crud import get_scheme_outputs
        outputs = await get_scheme_outputs(db, scheme_id)

        for output in outputs:
            amount = output.quantity * data.amount_done
            detail_data = DetailTopup(article=output.detail_article, amount=amount)
            await topup_detail(db, detail_data)
            await recount_availability(db, output.detail_article)

        components = await get_components(db, task.detail_article)
        for component in components:
            topdown_data = DetailTopup(
                article=component.child_article,
                amount=component.quantity * data.amount_done
            )
            await topdown_detail(db, topdown_data)

        return task

    if task.department == 'упаковка':
        order_data = OrderTopup(id=task.order_id, amount_done=data.amount_done)
        await topup_order(db, order_data)
    else:
        detail_data = DetailTopup(article=task.detail_article, amount=data.amount_done)
        await topup_detail(db, detail_data)

    detail_components = await get_components(db, task.detail_article)
    for component in detail_components:
        topdown_data = DetailTopup(
            article=component.child_article,
            amount=component.quantity * data.amount_done
        )
        await topdown_detail(db, topdown_data)

    await recount_availability(db, task.detail_article)

    return task


async def get_potential_order_tasks(db: AsyncSession, data) -> list:
    article = data.good_article
    quantity = data.quantity
    components = await get_good_components(db, article)
    details = []
    result = {}
    deficit = {}

    for component in components:
        root_detail = await get_detail(db, component.detail_article)
        await recount_availability(db, root_detail.article)
        details.append((root_detail, quantity * component.quantity))
        details += await get_all_components_list(db, component.detail_article, quantity * component.quantity)

    # Суммируем все quantity по деталям
    totals = {}
    for detail in details:
        art = detail[0].article
        if art not in totals:
            totals[art] = {'detail': detail[0], 'quantity': 0}
        totals[art]['quantity'] += detail[1]

    # Один раз обрабатываем каждую деталь
    for art, data in totals.items():
        detail_obj = data['detail']
        total_qty = data['quantity']
        availability = await _count_availability(db, art)
        await update_availability(db, art, availability)

        is_packaging = detail_obj.department == 'упаковка'
        amount_needed = total_qty if is_packaging else total_qty - detail_obj.stock

        components_of_detail = await get_components(db, art)

        if not components_of_detail:
            if amount_needed > 0 and not is_packaging:  # <-- фикс
                deficit[art] = amount_needed
        else:
            if amount_needed > 0:
                result[art] = {
                    'detail_article': art,
                    'detail_name': detail_obj.name,
                    'amount_needed': amount_needed,
                    'available': availability,
                    'department': detail_obj.department,
                    'posts': await get_detail_posts(db, art),
                }

    if deficit:
        from domains.cutting.service import find_best_cutting_plan
        from domains.cutting.crud import get_scheme_by_id

        cutting_plan = await find_best_cutting_plan(db, deficit)
        for scheme_id, times in cutting_plan.items():
            scheme_inputs = await get_components(db, -scheme_id)
            for inp in scheme_inputs:
                if inp.child_article in deficit:
                    deficit[inp.child_article] = inp.quantity * times

        cutting_plan = await find_best_cutting_plan(db, deficit)

        for scheme_id, times in cutting_plan.items():
            scheme = await get_scheme_by_id(db, scheme_id)
            key = f"cutting_{scheme_id}"
            result[key] = {
                'detail_article': 0 - scheme_id,
                'detail_name': f"Раскрой схема №{scheme_id} ({scheme.pipe_name})",
                'amount_needed': times,
                'available': 0,
                'department': 'сварка/резка',
                'posts': [scheme.post],
            }

            scheme_inputs = await get_components(db, -scheme_id)
            for inp in scheme_inputs:
                if inp.child_article in deficit:
                    continue
                input_detail = await get_detail(db, inp.child_article)
                input_amount_needed = inp.quantity * times
                availability = await _count_availability(db, inp.child_article)
                await update_availability(db, inp.child_article, availability)
                art = inp.child_article
                if art in result:
                    result[art]['amount_needed'] += input_amount_needed
                else:
                    result[art] = {
                        'detail_article': art,
                        'detail_name': input_detail.name,
                        'amount_needed': input_amount_needed,
                        'available': availability,
                        'department': input_detail.department,
                        'posts': await get_detail_posts(db, art),
                    }

    return list(result.values())


async def delete_task(db: AsyncSession, id: int) -> None:
    await crud.delete_task(db, id)