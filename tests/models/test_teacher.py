from db_interface.models.teacher import Teacher
from tests.database_test_case import DatabaseTestCase


class TestTeacher(DatabaseTestCase):
    def test_init(self):
        email = 'email@email.com'
        password = 'password'
        teacher = Teacher(password=password, email=email)
        self.assertEqual(teacher.email, email)
        self.assertEqual(teacher.password, password)

    def test_commit(self):
        teacher = Teacher(password='pw', email='email')
        self.session.add(teacher)
        self.session.commit()
        answer = self.session.query(Teacher).first()
        self.assertEqual(answer, teacher)
        self.assertIsInstance(answer.teacher_id, int)

    def test_get_json(self):
        teacher = Teacher(password='pw', email='email')
        self.assertEqual(teacher.get_json(), {'teacher_id': None, 'email': 'email'})

        self.session.add(teacher)
        self.session.commit()
        current_id = teacher.teacher_id
        self.assertEqual(teacher.get_json(), {'teacher_id': current_id, 'email': 'email'})
