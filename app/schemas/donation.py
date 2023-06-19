from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class DonationBase(BaseModel):
    full_amount: int
    comment: Optional[str]
    
    @validator('full_amount')
    def check_new_amount_not_less_than_invested(cls, value):
        """Сумма пожертвования должна быть больше 0."""
        if value < 1:
            raise ValueError('Сумма пожертвования должно быть больше 0')
        return value


class DonationDB(DonationBase):
    id: int
    user_id: Optional[str]
    invested_amount: int = Field(0)
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationCreate(DonationBase):
    class Config:
        orm_mode = True


class UserDonationRead(DonationBase):
    create_date: datetime
    id: int

    class Config:
        orm_mode = True
