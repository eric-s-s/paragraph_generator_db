from sqlalchemy import Column, Integer, String

from db_interface.models.base import Base


class Teacher(Base):
    __tablename__ = 'teacher'

    teacher_id = Column(Integer, primary_key=True)
    email = Column(String(50))
    password = Column(String(50))

    def get_json(self):
        return {
            'teacher_id': self.teacher_id,
            'email': self.email
        }
