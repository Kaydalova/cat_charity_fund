from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_fully_invested,
                                check_charity_project_invested_no_money,
                                check_name_duplicate, check_new_full_amount)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.find_sources import find_sources
from app.services.invest import invest_money_into_project

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(charity_project.name, session)

    new_project = await charity_project_crud.create(charity_project, session)

    sources = await find_sources(session, Donation)
    if sources:
        changed_sources = invest_money_into_project(
            target=new_project, sources=sources)
        session.add(*changed_sources)
    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude={'close_date'})
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session)

    await check_charity_project_fully_invested(charity_project)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount and charity_project.invested_amount:
        charity_project = await check_new_full_amount(charity_project, obj_in)
    charity_project = await charity_project_crud.update(charity_project, obj_in, session)
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)])
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session)):
    charity_project = await check_charity_project_exists(charity_project_id, session)
    await check_charity_project_invested_no_money(charity_project_id, session)
    await check_charity_project_fully_invested(charity_project)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project
