from sqlalchemy.orm import Session

from db_interface.models.user import User, UserType


class DBRequestHandler(object):
    def __init__(self, session: Session):
        self.session = session

    def create_teacher(self, email, password):
        teacher = User(email=email, password=password, user_type=UserType.TEACHER)
        self.session.add(teacher)
        self.session.commit()
        return teacher

    def create_student(self, email, password, score=0):
        student = User(email, password, UserType.STUDENT, score)
        self.session.add(student)
        self.session.commit()
        return student


