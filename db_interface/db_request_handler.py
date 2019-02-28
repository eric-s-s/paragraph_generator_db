from functools import wraps

from sqlalchemy.orm import Session

from db_interface.models.nouns import CountableNoun, UncountableNoun, StaticNoun
from db_interface.models.student import Student
from db_interface.models.teacher import Teacher
from db_interface.models.verb import Verb
from db_interface.models.word import Word, Tag


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
        return self._commit_and_get_json(teacher)

    def create_student(self, password: str, email: str = None, score: int = 0) -> dict:
        student = Student(password=password, email=email, score=score)
        return self._commit_and_get_json(student)

    def create_preposition(self, preposition: str) -> dict:
        word = Word(value=preposition, tag=Tag.PREPOSITION)
        return self._commit_and_get_json(word)

    def create_particle(self, particle: str) -> dict:
        word = Word(value=particle, tag=Tag.PARTICLE)
        return self._commit_and_get_json(word)

    def create_verb(self, value: str, irregular_past: str = '') -> dict:
        verb = Verb(value=value, irregular_past=irregular_past)
        return self._commit_and_get_json(verb)

    def create_countable_noun(self, value: str, irregular_plural: str = '') -> dict:
        noun = CountableNoun(value=value, irregular_plural=irregular_plural)
        return self._commit_and_get_json(noun)

    def create_uncountable_noun(self, value: str) -> dict:
        noun = UncountableNoun(value=value)
        return self._commit_and_get_json(noun)

    def create_static_noun(self, value: str, is_plural: bool) -> dict:
        noun = StaticNoun(value=value, is_plural=is_plural)
        return self._commit_and_get_json(noun)

    def _commit_and_get_json(self, value):
        self.session.add(value)
        self.session.commit()
        return value.get_json()

    def get_student(self, student_id: int) -> dict:
        student = self._get_database_object_from_id(student_id, Student)
        return student.get_json()

    def get_teacher(self, teacher_id: int) -> dict:
        teacher = self._get_database_object_from_id(teacher_id, Teacher)
        return teacher.get_json()

    def get_particle_or_preposition(self, id_: int) -> dict:
        return self._get_database_object_from_id(id_, Word).get_json()

    def get_verb(self, id_: int) -> dict:
        return self._get_database_object_from_id(id_, Verb).get_json()

    def get_countable_noun(self, id_):
        return self._get_database_object_from_id(id_, CountableNoun).get_json()

    def get_uncountable_noun(self, id_: int) -> dict:
        return self._get_database_object_from_id(id_, UncountableNoun).get_json()

    def get_static_noun(self, id_: int) -> dict:
        return self._get_database_object_from_id(id_, StaticNoun).get_json()

    def _get_database_object_from_id(self, id_, class_):
        id_attribute = {Student: 'student_id', Teacher: 'teacher_id', Word: 'id', Verb: 'id', CountableNoun: 'id',
                        UncountableNoun: 'id', StaticNoun: 'id'}
        kwargs = {id_attribute[class_]: id_}
        db_object = self.session.query(class_).filter_by(**kwargs).first()
        if db_object is None:
            raise BadIdError(f'{id_attribute[class_]}: {id_} does not exist')
        return db_object

    def get_all_prepositions_and_particles(self):
        return self._get_all_jsons(Word)

    def get_all_verbs(self):
        return self._get_all_jsons(Verb)

    def get_all_countable_nouns(self):
        return self._get_all_jsons(CountableNoun)

    def get_all_uncountable_nouns(self):
        return self._get_all_jsons(UncountableNoun)

    def get_all_static_nouns(self):
        return self._get_all_jsons(StaticNoun)

    def _get_all_jsons(self, class_):
        return [word.get_json() for word in self.session.query(class_)]

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

    def update_score(self, student_id: int, new_score: int) -> dict:
        student = self._get_database_object_from_id(student_id, Student)
        student.score = new_score
        self.session.commit()
        return student.get_json()
