import enum

from sqlalchemy import Column, String, Enum, Integer, UniqueConstraint

from db_interface.models.base import Base


class Tag(enum.Enum):
    PREPOSITION = enum.auto()
    PARTICLE = enum.auto()


class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    value = Column(String(30), nullable=False)
    tag = Column(Enum(Tag), nullable=False)
    UniqueConstraint(value, tag)

    def get_json(self):
        return {
            'id': self.id,
            'value': self.value,
            'tag': self.tag.name
        }
