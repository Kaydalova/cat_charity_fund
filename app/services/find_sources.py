from typing import List, Union

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def find_sources(
        session: AsyncSession,
        model: Union[Donation, CharityProject]
) -> List[Union[Donation, CharityProject]]:
    """
    Функция проверяет есть ли незакрытые благотворительные проекты/пожертвования
    и возвращает их список сортированный по id (в порядке добавления).
    """
    sources = await session.execute(
        select(model).where(
            model.fully_invested == 0).order_by(
                desc(model.id)))
    return sources.scalars().all()
