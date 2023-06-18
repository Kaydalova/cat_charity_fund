from app.models import Donation

from app.crud.base import CRUDBase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDDonation(CRUDBase):
    async def get_users_donations(self, user_id: int, session: AsyncSession):
        user_donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id))
        return user_donations.scalars().all()

donation_crud = CRUDDonation(Donation)