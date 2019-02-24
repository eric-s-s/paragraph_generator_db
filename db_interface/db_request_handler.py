from sqlalchemy.orm import Session

from db_interface.models.student import User, UserType


class BadId(ValueError):
    pass


class DBRequestHandler(object):
    def __init__(self, session: Session):
        self.session = session

    def create_teacher(self, email, password):
        teacher = User(password=password, user_type=UserType.TEACHER, email=email)
        self.session.add(teacher)
        self.session.commit()
        return teacher.get_json()

    def create_student(self, email, password, score=0):
        student = User(password, UserType.STUDENT, email, score)
        self.session.add(student)
        self.session.commit()
        return student.get_json()

    def get_user(self, user_id):
        raise BadId('oops')
