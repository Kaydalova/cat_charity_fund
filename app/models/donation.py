from app.models.base_charity import BaseCharity
from sqlalchemy import Column, Text, ForeignKey, Integer


class Donation(BaseCharity):
    """ Модель благотворительных пожертвований"""
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'))
    comment = Column(Text, nullable=True)