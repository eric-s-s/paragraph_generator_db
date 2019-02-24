from sqlalchemy import Column, Integer, String

from db_interface.models.base import Base


class Student(Base):
    __tablename__ = 'student'
    student_id = Column(Integer, primary_key=True)

    email = Column(String(50), nullable=True, unique=True)
    password = Column(String(30), nullable=False)
    score = Column(Integer, nullable=False)

    def __init__(self, password, email=None, score=0):
        self.email = email
        self.password = password
        self.score = score

    def get_json(self):
        return {
            'email': self.email,
            'score': self.score,
            'student_id': self.student_id
        }
