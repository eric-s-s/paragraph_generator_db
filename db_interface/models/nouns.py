from sqlalchemy import Column, String, Integer, Boolean

from db_interface.models.base import Base


class CountableNoun(Base):
    __tablename__ = 'countable_noun'
    id = Column(Integer, primary_key=True)

    value = Column(String(30), nullable=False, unique=True)
    irregular_plural = Column(String(30), nullable=False)


class UncountableNoun(Base):
    __tablename__ = 'uncountable_noun'
    id = Column(Integer, primary_key=True)

    value = Column(String(30), nullable=False, unique=True)


class StaticNoun(Base):
    __tablename__ = 'static_noun'
    id = Column(Integer, primary_key=True)

    value = Column(String(30), nullable=False, unique=True)
    is_plural = Column(Boolean, nullable=False)
