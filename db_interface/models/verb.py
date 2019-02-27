from sqlalchemy import Column, Integer, String, UniqueConstraint

from db_interface.models.base import Base


class Verb(Base):
    __tablename__ = 'verb'

    id = Column(Integer, primary_key=True)

    value = Column(String(30), nullable=False)
    irregular_past = Column(String(30), nullable=False)
    UniqueConstraint(value, irregular_past)

    def __init__(self, value, irregular_past=''):
        self.value = value
        self.irregular_past = irregular_past

    def get_json(self):
        return {
            'id': self.id,
            'value': self.value,
            'irregular_past': self.irregular_past
        }
