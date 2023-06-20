from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationDB(DonationBase):
    comment: Optional[str]
    create_date: datetime
    full_amount: PositiveInt
    id: int
    user_id: Optional[int]
    invested_amount: int = Field(0)
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationCreate(DonationBase):
    pass


class UserDonationRead(DonationBase):
    create_date: datetime
    id: int

    class Config:
        orm_mode = True
