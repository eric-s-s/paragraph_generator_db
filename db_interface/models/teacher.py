from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db_interface.models.base import Base


class Teacher(Base):
    __tablename__ = 'teacher'

    teacher_id = Column(Integer, primary_key=True)
    email = Column(String(50))
    password = Column(String(50))
    current_word_list_id = Column(Integer, ForeignKey('word_list.id', ondelete='CASCADE'))

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.current_word_list = None

