from functools import wraps

from sqlalchemy.orm import Session

from db_interface.models.student import Student
from db_interface.models.teacher import Teacher


class NotFoundError(ValueError):
    pass


class BadIdError(ValueError):
    pass

# TODO delete???
def raises_bad_id_error(method):
    @wraps(method)
    def new_method(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except AttributeError:
            raise BadIdError(f'id in {args} or {kwargs} does not exits')
    return new_method


class DBRequestHandler(object):
    def __init__(self, session: Session):
        self.session = session

    def create_teacher(self, password: str, email: str) -> dict:
        teacher = Teacher(password=password, email=email)
        self.session.add(teacher)
        self.session.commit()
        return teacher.get_json()

    def create_student(self, password: str, email: str = None, score: int = 0) -> dict:
        student = Student(password=password, email=email, score=score)
        self.session.add(student)
        self.session.commit()
        return student.get_json()

    def get_student_id(self, email: str) -> int:
        student = self._get_user_id(email, class_=Student)
        return student.student_id

    def get_teacher_id(self, email: str) -> int:
        teacher = self._get_user_id(email, class_=Teacher)
        return teacher.teacher_id

    def _get_user_id(self, email, class_):
        user = self.session.query(class_).filter(class_.email == email).first()
        if user is None:
            raise NotFoundError(f'{class_.__name__} with email: {email} not found.')
        return user

    def is_student_login_correct(self, id_: int, password: str) -> bool:
        student = self._get_database_object_from_id(id_, Student)
        return student.password == password

    def is_teacher_login_correct(self, id_: int, password: str) -> bool:
        teacher = self._get_database_object_from_id(id_, Teacher)
        return teacher.password == password

    def get_student(self, student_id: int) -> dict:
        student = self._get_database_object_from_id(student_id, Student)
        return student.get_json()

    def get_teacher(self, teacher_id):
        teacher = self._get_database_object_from_id(teacher_id, Teacher)
        return teacher.get_json()

    def _get_database_object_from_id(self, id_, class_):
        keyword = {Student: 'student_id', Teacher: 'teacher_id'}
        kwargs = {keyword[class_]: id_}
        db_object = self.session.query(class_).filter_by(**kwargs).first()
        if db_object is None:
            raise BadIdError(f'{keyword[class_]}: {id_} does not exist')
        return db_object

    def update_score(self, student_id, new_score):
        student = self._get_database_object_from_id(student_id, Student)
        student.score = new_score
        self.session.commit()
        return student.get_json()
