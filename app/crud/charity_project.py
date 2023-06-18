from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)


async def create_charity_project(
        new_project: CharityProjectCreate,
        session: AsyncSession) -> CharityProject:
    """
    Функция получает на вход pydantic схему CharityProjectCreate,
    преобразует ее в словарь, а затем создает и возвращает
    новый объект CharityProject.
    """
    new_project_data = new_project.dict()
    db_project = CharityProject(**new_project_data)
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


async def get_project_id_by_name(
        project_name: str,
        session: AsyncSession) -> Optional[int]:
    """
    Функция возвращает id проекта, если проект с указанным именем существует.
    Если проект еще не создан - вернет None.
    """
    project_name_id = await session.execute(
        select(CharityProject.id).where(
            CharityProject.name == project_name))
    return project_name_id.scalars().first()


async def read_all_projects_from_db(
        session: AsyncSession) -> List[CharityProject]:
    """
    Функция возвращает список всех благотворительных проектов.
    """
    all_projects = await session.execute(select(CharityProject))
    return all_projects.scalars().all()


async def get_charity_project_by_id(
        project_id: int,
        session: AsyncSession) -> Optional[CharityProject]:
    """
    Функция проверяет есть ли проект с указанным id в базе.
    :param project_id: целое число, id искомого проекта
    :param session: асинхронная сессия
    :return: объект класса CharityProject или None
    """
    project = await session.execute(
        select(CharityProject).where(
            CharityProject.id == project_id))
    return project.scalars().first()


async def update_charity_project(
        db_project: CharityProject,
        project_in: CharityProjectUpdate,
        session: AsyncSession) -> CharityProject:
    """
    Функция получает на вход объект из базы, который нужно изменить
    и поля:значения, которыми нужно обновить объект.
    :param db_project: объект модели CharityProject для изменения
    :param project_in: данные для изменения
    :param session: асинхронная сессия
    :return: обновленный объект класса CharityProject
    """
    obj_data = jsonable_encoder(db_project)
    update_data = project_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_project, field, update_data[field])
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


async def delete_charity_project(
        db_project: CharityProject,
        session: AsyncSession) -> CharityProject:
    await session.delete(db_project)
    await session.commit()
    return db_project
