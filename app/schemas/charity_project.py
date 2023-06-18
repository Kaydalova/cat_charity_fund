from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(..., min_length=2, max_length=100)
    description: Optional[str]
    full_amount: Optional[int]
    @validator('full_amount')
    def check_new_amount_not_less_than_invested(cls, value):
        """Сумма сбора должна быть больше 0."""
        if value < 1:
            raise ValueError('Сумма сбора должно быть больше 0')
        return value


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=2, max_length=100)
    description: str
    full_amount: int


class CharityProjectDB(BaseModel):
    name: str
    description: str
    full_amount: int
    id: int
    invested_amount: Optional[int]
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    pass
