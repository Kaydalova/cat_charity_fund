from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.constants import CHARITY_PROJECT_MIN, CHARITY_PROJECT_NAME_MAX


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=CHARITY_PROJECT_MIN,
        max_length=CHARITY_PROJECT_NAME_MAX)
    description: Optional[str] = Field(
        None, min_length=CHARITY_PROJECT_MIN)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=CHARITY_PROJECT_MIN,
        max_length=CHARITY_PROJECT_NAME_MAX)
    description: str = Field(
        ..., min_length=CHARITY_PROJECT_MIN)
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    pass
