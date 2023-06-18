from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Donation
from sqlalchemy import select
from typing import List
from app.schemas.charity_project import CharityProjectCreate
import datetime


async def invest_free_money_in_new_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession) -> CharityProjectCreate:
    free_money = await check_money_for_investing(session)
    print(f'free_money {free_money}')
    if free_money:
        charity_project_needs_money = await gather_money_for_new_project(
            charity_project, free_money[::-1], session)
        print(f'charity_project_needs_money - {charity_project_needs_money}')
        if charity_project_needs_money:
            charity_project.invested_amount = (
                    charity_project.full_amount - charity_project_needs_money)
        else:
            charity_project.invested_amount = charity_project.full_amount
            charity_project.fully_invested = True
            charity_project.close_date = datetime.datetime.now()
    return charity_project


async def check_money_for_investing(session: AsyncSession) -> List[Donation]:
    """
    Функция проверяет есть ли в проекте неалоцированные средства
    и возвращает список объектов Donation в которых они есть.
    """
    free_money = await session.execute(
        select(Donation).where(Donation.fully_invested == 0))
    return free_money.scalars().all()


async def gather_money_for_new_project(
        charity_project: CharityProjectCreate,
        free_money: List[Donation],
        session: AsyncSession) -> int:
    """Функция распределяет свободные средства в новый проект
    и возвращает остаток, необходимый для полного закрытия проекта."""
    charity_project_needs_money = charity_project.full_amount
    print(f'charity_project_needs_money {charity_project_needs_money}')
    while charity_project_needs_money and free_money:
        donation = free_money.pop()
        surplus = donation.full_amount - donation.invested_amount

        if surplus < charity_project_needs_money:
            charity_project_needs_money -= surplus
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            donation.close_date = datetime.datetime.now()
            session.add(donation)
        elif surplus > charity_project_needs_money:
            donation.invested_amount -= charity_project_needs_money
            charity_project_needs_money = 0
            session.add(donation)
        else:  #surplus = charity_project_needs_money
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            donation.close_date = datetime.datetime.now()
            charity_project_needs_money = 0
            session.add(donation)

    await session.commit()
    return charity_project_needs_money
















