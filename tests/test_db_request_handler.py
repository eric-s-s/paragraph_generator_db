from db_interface.db_request_handler import DBRequestHandler
from db_interface.models.user import User, UserType
from tests.database_test_case import DatabaseTestCase


class MyTestCase(DatabaseTestCase):

    def setUp(self):
        super(MyTestCase, self).setUp()
        self.request_handler = DBRequestHandler(self.session)

    def test_init(self):
        request_handler = DBRequestHandler(self.session)
        self.assertIs(request_handler.session, self.session)

    def test_create_teacher(self):
        email = 'eric@email.com'
        pass_word = 'password'
        response = self.request_handler.create_teacher(email, pass_word)
        created_user = self.session.query(User).filter_by(email=email)[0]
        self.assertIs(response, created_user)
        self.assertEqual(created_user.score, 0)
        self.assertEqual(created_user.user_type, UserType.TEACHER)
        self.assertEqual(created_user.password, pass_word)
        self.assertEqual(created_user.email, email)

    def test_create_student_default_score(self):
        email = 'a@b'
        password = 'pw'
        response = self.request_handler.create_student(email, password)
        created_user = self.session.query(User).filter_by(email=email)[0]
        self.assertIs(response, created_user)
        self.assertEqual(created_user.email, email)
        self.assertEqual(created_user.password, password)
        self.assertEqual(created_user.user_type, UserType.STUDENT)
        self.assertEqual(created_user.score, 0)

    def test_create_student_non_default_score(self):
        email = 'a@b'
        password = 'a'
        score = 100
        response = self.request_handler.create_student(email, password, score)
        created_user = self.session.query(User).filter_by(email=email)[0]
        self.assertIs(response, created_user)
        self.assertEqual(created_user.score, score)
