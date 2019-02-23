import enum

from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum as SQLEnum

from db_interface.models.base import Base


class UserType(enum.Enum):
    TEACHER = enum.auto()
    STUDENT = enum.auto()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)

    user_name = Column(String(30), unique=True, nullable=False)
    score = Column(Integer, nullable=False)
    privileges = Column(SQLEnum(UserType), nullable=False)

    def __init__(self, user_name, user_type, score=0):
        self.user_name = user_name
        self.score = score
        self.privileges = user_type
