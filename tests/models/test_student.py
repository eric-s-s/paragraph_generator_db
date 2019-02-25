from sqlalchemy.exc import IntegrityError

from db_interface.models.student import Student
from tests.database_test_case import DatabaseTestCase


class TestStudent(DatabaseTestCase):
    def test_init(self):
        email = 'email@email.com'
        password = 'password'
        score = 243758
        student = Student(password=password, email=email, score=score)
        self.assertEqual(student.email, email)
        self.assertEqual(student.password, password)
        self.assertEqual(student.score, score)

    def test_init_score_defaults_to_zero(self):
        student = Student(password='pw', email='email')
        self.assertEqual(student.score, 0)

    def test_init_email_defaults_to_None(self):
        student = Student(password='pw')
        self.assertIsNone(student.email)

    def test_commit_all_fields(self):
        student = Student(password='pw', email='email', score=0)
        self.session.add(student)
        self.session.commit()
        answer = self.session.query(Student).first()
        self.assertEqual(answer, student)
        self.assertIsInstance(answer.student_id, int)

    def test_commit_with_default_score(self):
        student = Student(password='pw', email='email')
        self.session.add(student)
        self.session.commit()
        answer = self.session.query(Student).first()
        self.assertEqual(answer, student)
        self.assertEqual(answer.score, 0)

    def test_commit_with_default_email(self):
        student = Student(password='pw', score=1)
        self.session.add(student)
        self.session.commit()
        answer = self.session.query(Student).first()
        self.assertEqual(answer, student)
        self.assertIsNone(answer.email)

    def test_email_unique_constraint(self):
        email = 'email@email.com'
        student = Student(password='a', email=email, score=1)
        same_student_name = Student(password='b', email=email, score=2)
        self.session.add_all([student, same_student_name])
        self.assertRaises(IntegrityError, self.session.commit)

    def test_email_unique_constraint_allows_multiple_None_values(self):
        password = 'a'
        score = 1
        student = Student(password=password, score=score)
        other_student = Student(password=password, score=score)
        self.session.add_all((student, other_student))
        student_list = self.session.query(Student).all()
        self.assertEqual(len(student_list), 2)
        self.assertNotEqual(student_list[0].student_id, student_list[1].student_id)

    def test_password_score_not_unique(self):
        password = 'pw'
        score = 100
        first = Student(password=password, email='a', score=score)
        second = Student(password=password, email='b', score=score)
        self.session.add_all([first, second])
        self.assertIsNone(self.session.commit())

    def test_email_nullable(self):
        student = Student(password='pw', email=None, score=0)
        self.session.add(student)
        self.assertIsNone(self.session.commit())

    def test_all_fields_but_email_not_nullable(self):
        class_ = Student
        keys = ('password', 'score')
        values = ('random', 398)
        self.assert_not_nullable(class_, keys, values)

    def test_get_json_student(self):
        email = 'email'
        password = 'pw'
        score = 10

        student = Student(password, email, score)
        self.session.add(student)
        self.session.commit()
        expected = {
            'email': email,
            'score': score,
            'student_id': student.student_id
        }
        self.assertEqual(student.get_json(), expected)
