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
        user_name = 'random'
        score = 243758
        privileges = UserType.TEACHER
        user = User(user_name=user_name, score=score, user_type=privileges)
        self.assertEqual(user.user_name, user_name)
        self.assertEqual(user.score, score)
        self.assertEqual(user.privileges, privileges)

    def test_init_score_defaults_to_zero(self):
        user = User(user_name='joe', user_type=UserType.TEACHER)
        self.assertEqual(user.score, 0)

    def test_commit_all_fields(self):
        user = User(user_name='joe', score=0, user_type=UserType.STUDENT)
        self.session.add(user)
        self.session.commit()
        answer = self.session.query(User).all()[0]
        self.assertEqual(answer, user)
        self.assertIsInstance(answer.id, int)

    def test_commit_with_default_score(self):
        user = User(user_name='Ethel', user_type=UserType.STUDENT)
        self.session.add(user)
        self.session.commit()
        answer = self.session.query(User).all()[0]
        self.assertEqual(answer, user)
        self.assertEqual(answer.score, 0)

    def test_user_name_unique_constraint(self):
        user_name = 'a'
        user = User(user_name=user_name, user_type=UserType.STUDENT)
        same_user_name = User(user_name=user_name, user_type=UserType.TEACHER)
        self.session.add_all([user, same_user_name])
        self.assertRaises(IntegrityError, self.session.commit)

    def test_score_and_user_type_not_unique(self):
        score = 100
        privileges = UserType.TEACHER
        first = User(user_name='a', score=score, user_type=privileges)
        second = User(user_name='b', score=score, user_type=privileges)
        self.session.add_all([first, second])
        self.assertIsNone(self.session.commit())

    def test_all_fields_not_nullable(self):
        class_ = User
        keys = ('user_name', 'score', 'user_type')
        values = ('random', 398, UserType.TEACHER)
        self.assert_not_nullable(class_, keys, values)

