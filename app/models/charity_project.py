from sqlalchemy import Column, String, Text
from app.models.base_charity import BaseCharity

class CharityProject(BaseCharity):
    """ Модель благотворительных проектов"""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)







