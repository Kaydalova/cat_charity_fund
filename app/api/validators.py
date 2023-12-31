""" Функции для проверки данных"""
import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (DELETION_NOT_ALLOWED, INVALID_FULL_AMOUNT,
                           PATCH_NOT_ALLOWED, PROJECT_NAME_ALREADY_EXISTS,
                           PROJECT_NOT_FOUND)
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    """
    Проверяет не занято ли указанное имя проекта.
    """
    if await charity_project_crud.get_object_id_by_name(
            project_name, CharityProject, session):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_NAME_ALREADY_EXISTS)


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession) -> CharityProject:
    """
    Проверяет существует ли благотворительный проект по указанному id.
    """
    charity_project = await charity_project_crud.get(project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND)
    return charity_project


async def check_charity_project_invested_no_money(
        project_id: int, session: AsyncSession) -> None:
    """
    Выполняет проверку, были ли инвестиции в указанный проект.
    """
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=DELETION_NOT_ALLOWED)


async def check_charity_project_fully_invested(
        charity_project: CharityProject) -> None:
    """
    Функция проверяет был ли проект инвестирован полностью.
    """
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail=PATCH_NOT_ALLOWED)


async def check_new_full_amount(
        charity_project: CharityProject,
        obj_in: CharityProjectUpdate) -> CharityProject:
    """
    Функция проверяет, что новая сумма пожертвований на проекте
    не меньше уже внесенной.
    Если новая целевая сумма равна уже сделанным пожертвованиям,
    статус проекта меняется на fully_invested и присавивается close_date.
    """

    if charity_project.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=INVALID_FULL_AMOUNT)

    if charity_project.invested_amount == obj_in.full_amount:
        charity_project.fully_invested = True
        charity_project.close_date = datetime.datetime.now()
    return charity_project
