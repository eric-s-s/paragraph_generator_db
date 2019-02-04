import enum

from sqlalchemy import Column, String, Enum, Integer, UniqueConstraint

from db_interface.models.base import Base


class Tag(enum.Enum):
    PREPOSITION = 'PREPOSITION'
    PARTICLE = 'PARTICLE'


class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    value = Column(String(30), nullable=False)
    tag = Column(Enum(Tag), nullable=False)
    UniqueConstraint(value, tag)
