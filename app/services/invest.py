import datetime
from typing import List, Union

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_money_into_project(
        new_item: Union[Donation, CharityProject],
        session: AsyncSession
) -> None:
    if type(new_item) == Donation:
        model = CharityProject
    else:
        model = Donation
    print(f'model = {model}')
    ready_for_investing = await check_ready_for_investing(
        session=session, model=model)
    print(f'ready_for_investing {ready_for_investing}')
    if ready_for_investing:
        print('ready')
        await allocate_money(new_item, ready_for_investing, session)


async def allocate_money(
        new_item: Union[Donation, CharityProject],
        ready_for_investing: List[Union[Donation, CharityProject]],
        session: AsyncSession):
    needs_investing = new_item.full_amount
    print(f'needs_investing {needs_investing}')
    while needs_investing and ready_for_investing:
        invest_space = ready_for_investing.pop()
        print(f'invest_space {invest_space}')
        surplus = invest_space.full_amount - invest_space.invested_amount
        print(f'surplus ={surplus}')

        if surplus < needs_investing:
            await item_set_fully_invested(invest_space, session)
            needs_investing -= surplus
            new_item.invested_amount += surplus
        elif surplus > needs_investing:
            invest_space.invested_amount += needs_investing
            await item_set_fully_invested(new_item, session)
            needs_investing = 0
            session.add(invest_space)
        else:  # surplus = money_to_allocate
            needs_investing = 0
            await item_set_fully_invested(invest_space, session)
            await item_set_fully_invested(new_item, session)

    session.add(new_item)
    await session.commit()
    return needs_investing


async def item_set_fully_invested(
        item: Union[Donation, CharityProject],
        session: AsyncSession) -> None:
    item.invested_amount = item.full_amount
    item.fully_invested = True
    item.close_date = datetime.datetime.now()
    session.add(item)


async def check_ready_for_investing(
        session: AsyncSession,
        model: Union[Donation, CharityProject]
) -> List[Union[Donation, CharityProject]]:
    """
    Функция проверяет есть ли незакрытые благотворительные проекты/пожертвования
    и возвращает их список сортированный в порядке добавления.
    """
    ready_for_investing = await session.execute(
        select(model).where(
            model.fully_invested is None).order_by(
                desc(model.create_date)))
    return ready_for_investing.scalars().all()
