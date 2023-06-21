from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, UserDonationRead
from app.services.find_sources import find_sources
from app.services.invest import invest_money_into_project

router = APIRouter()


@router.get('/', response_model=List[DonationDB], response_model_exclude={'close_date'})
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    """Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={
        'user_id', 'fully_invested',
        'invested_amount', 'close_date'})
async def create_new_donation(
        new_donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(new_donation, session, user)

    sources = await find_sources(session, CharityProject)
    if sources:
        changed_sources = invest_money_into_project(
            target=new_donation, sources=sources)
        session.add(*changed_sources)
    await session.commit()

    await session.refresh(new_donation)
    return new_donation


@router.get('/my', response_model=List[UserDonationRead])
async def get_my_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)):
    """Получить список моих пожертвований."""
    user_donations = await donation_crud.get_users_donations(user.id, session)
    return user_donations
