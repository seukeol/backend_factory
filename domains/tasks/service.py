from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .model import Task
from .schema import TaskEdit, TaskGetFilter, TaskTopup
from domains.orders.service import topup_order
from domains.orders.schema import OrderTopup
from domains.details.schema import DetailTopup
from domains.details.service import topup_detail, get_parents
from domains.bom.service import recount_availability, get_all_parents_list, _count_availability
from ..details.crud import topdown_detail
from ..goods.crud import get_good_components
from domains.posts.crud import get_posts

async def get_task(db: AsyncSession, id: int) -> Task | None:
    return await crud.get_task(db, id)


async def get_tasks(db: AsyncSession, filter: TaskGetFilter) -> list[Task]:
    return await crud.get_tasks(db, filter)


async def get_tasks_for_order(db: AsyncSession, order_id: int) -> list[Task]:
    return await crud.get_tasks_for_order(db, order_id)


async def edit_task(db: AsyncSession, data: TaskEdit) -> None:
    await crud.edit_task(db, data)


async def topup_task(db: AsyncSession, data: TaskTopup) -> Task:
    task = await crud.topup_task(db, data)
    if task.amount_done >= task.amount_needed:
        task.result = True
    if task.department == 'упаковка':
        order_data = OrderTopup(id=task.order_id, amount_done=data.amount_done)
        await topup_order(db, order_data)
    else:
        detail_data = DetailTopup(article=task.detail_article, amount=data.amount_done)
        await topup_detail(db, detail_data)
    detail_parents = await get_parents(db, task.detail_article)
    for parent in detail_parents:
        topdown_data = DetailTopup(article=parent.detail_article, amount=parent.quantity*data.amount_done)
        await topdown_detail(db, topdown_data)
    await recount_availability(db, task.detail_article)
    return task


async def get_potential_order_tasks(db: AsyncSession, data) -> list:
    good_id = data.good_id
    quantity = data.quantity

    components = await get_good_components(db, good_id)
    details = []
    result = []
    for component in components:
        details+= await get_all_parents_list(db, component.detail_article, quantity)
    for detail in details:
        task_info = {
            'detail_article': detail[0].detail_article,
            'detail_name': detail[0].detail_name,
            'amount_needed': detail[1],
            'available': await _count_availability(db, detail[0].detail_article),
            'department': detail[0].department,
            'posts': await get_posts(db, detail[0].department)
        }
        result.append(task_info)
    return result


async def delete_task(db: AsyncSession, id: int) -> None:
    await crud.delete_task(db, id)