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

    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(30), nullable=False)
    score = Column(Integer, nullable=False)
    user_type = Column(SQLEnum(UserType), nullable=False)

    def __init__(self, email, password, user_type, score=0):
        self.email = email
        self.password = password
        self.score = score
        self.user_type = user_type
