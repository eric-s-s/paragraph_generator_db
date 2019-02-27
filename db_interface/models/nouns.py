from sqlalchemy import Column, String, Integer, Boolean

from db_interface.models.base import Base


class CountableNoun(Base):
    __tablename__ = 'countable_noun'
    id = Column(Integer, primary_key=True)

    value = Column(String(30), nullable=False, unique=True)
    irregular_plural = Column(String(30), nullable=False)

    def __init__(self, value, irregular_plural=''):
        self.value = value
        self.irregular_plural = irregular_plural

    def get_json(self):
        return {
            'id': self.id,
            'value': self.value,
            'irregular_plural': self.irregular_plural
        }


class UncountableNoun(Base):
    __tablename__ = 'uncountable_noun'
    id = Column(Integer, primary_key=True)

    value = Column(String(30), nullable=False, unique=True)

    def get_json(self):
        return {
            'value': self.value,
            'id': self.id
        }


class StaticNoun(Base):
    __tablename__ = 'static_noun'
    id = Column(Integer, primary_key=True)

    value = Column(String(30), nullable=False, unique=True)
    is_plural = Column(Boolean, nullable=False)

    def get_json(self):
        return {
            'id': self.id,
            'value': self.value,
            'is_plural': self.is_plural
        }
