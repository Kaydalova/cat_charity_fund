from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from fastapi import HTTPException


async def check_name_duplicate(project_name: str, session: AsyncSession) -> None:
    if await charity_project_crud.get(project_name, session):
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!')


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден')
    return charity_project


async def check_charity_project_invested_no_money(
        project_id: int, session: AsyncSession) -> None:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=405,
            detail='Нельзя удалить проект, в который уже были выделены деньги')


async def check_charity_project_is_opened(
        project_id: int, session: AsyncSession) -> None:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.close_date:
        raise HTTPException(
            status_code=422,
            detail='Нельзя удалять закрытые проекты')
