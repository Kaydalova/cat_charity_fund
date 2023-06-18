from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import (create_charity_project,
                                      delete_charity_project,
                                      get_charity_project_by_id,
                                      get_project_id_by_name,
                                      read_all_projects_from_db,
                                      update_charity_project)
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)

router = APIRouter(prefix='/charity_project',
                   tags=['Charity Projects'])


@router.post(
    '/',
    response_model=CharityProjectDB)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)):
    await check_name_duplicate(charity_project.name, session)
    new_project = await create_charity_project(charity_project, session)
    return new_project


@router.get('/', response_model=List[CharityProjectDB])
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)):
    all_projects = await read_all_projects_from_db(session)
    return all_projects


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)):
    charity_project = await check_charity_project_exists(charity_project_id, session)
    if obj_in.name:
        check_name_duplicate(obj_in.name, session)
    charity_project = await update_charity_project(charity_project, obj_in, session)
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session)):
    charity_project = await check_charity_project_exists(charity_project_id, session)
    charity_project = await delete_charity_project(charity_project, session)
    return charity_project


async def check_name_duplicate(project_name: str, session: AsyncSession) -> None:
    if await get_project_id_by_name(project_name, session):
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!')


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession) -> CharityProject:
    charity_project = await get_charity_project_by_id(project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден')
    return charity_project
