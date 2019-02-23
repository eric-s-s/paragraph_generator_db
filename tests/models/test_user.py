import unittest

from sqlalchemy.exc import IntegrityError

from db_interface.models.user import UserType, User
from tests.database_test_case import DatabaseTestCase


class TestUserType(unittest.TestCase):
    def test_all_types(self):
        self.assertEqual(getattr(UserType, 'TEACHER'), UserType.TEACHER)
        self.assertEqual(getattr(UserType, 'STUDENT'), UserType.STUDENT)
        self.assertEqual(len(UserType.__members__), 2)


class TestUser(DatabaseTestCase):
    def test_init(self):
        email = 'email@email.com'
        password = 'password'
        score = 243758
        privileges = UserType.TEACHER
        user = User(email=email, password=password, user_type=privileges, score=score)
        self.assertEqual(user.email, email)
        self.assertEqual(user.password, password)
        self.assertEqual(user.score, score)
        self.assertEqual(user.user_type, privileges)

    def test_init_score_defaults_to_zero(self):
        user = User(email='email', password='pw', user_type=UserType.TEACHER)
        self.assertEqual(user.score, 0)

    def test_commit_all_fields(self):
        user = User(email='email', password='pw', score=0, user_type=UserType.STUDENT)
        self.session.add(user)
        self.session.commit()
        answer = self.session.query(User).all()[0]
        self.assertEqual(answer, user)
        self.assertIsInstance(answer.id, int)

    def test_commit_with_default_score(self):
        user = User(email='email', password='pw', user_type=UserType.STUDENT)
        self.session.add(user)
        self.session.commit()
        answer = self.session.query(User).all()[0]
        self.assertEqual(answer, user)
        self.assertEqual(answer.score, 0)

    def test_email_unique_constraint(self):
        email = 'email@email.com'
        user = User(email=email, password='a', user_type=UserType.STUDENT, score=1)
        same_user_name = User(email=email, password='b', user_type=UserType.TEACHER, score=2)
        self.session.add_all([user, same_user_name])
        self.assertRaises(IntegrityError, self.session.commit)

    def test_password_score_and_user_type_not_unique(self):
        password = 'pw'
        score = 100
        privileges = UserType.TEACHER

        first = User(email='a', password=password, score=score, user_type=privileges)
        second = User(email='b', password=password, score=score, user_type=privileges)
        self.session.add_all([first, second])
        self.assertIsNone(self.session.commit())

    def test_all_fields_not_nullable(self):
        class_ = User
        keys = ('email', 'password', 'score', 'user_type')
        values = ('email', 'random', 398, UserType.TEACHER)
        self.assert_not_nullable(class_, keys, values)
