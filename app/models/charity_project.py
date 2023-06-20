from sqlalchemy import Column, String, Text

from app.constants import CHARITY_PROJECT_NAME_MAX
from app.models.base_charity import BaseCharity


class CharityProject(BaseCharity):
    """ Модель благотворительных проектов"""
    name = Column(String(CHARITY_PROJECT_NAME_MAX), unique=True, nullable=False)
    description = Column(Text, nullable=False)
