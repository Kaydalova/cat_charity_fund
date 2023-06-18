import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class BaseCharity(Base):
    """ Базовая модель благотворительных проектов и пожертвований"""
    __abstract__ = True
    full_amount = Column(Integer)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.datetime.now)
    close_date = Column(DateTime)
