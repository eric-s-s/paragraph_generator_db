
from sqlalchemy.exc import IntegrityError

from db_interface.models.teacher import Teacher
from tests.database_test_case import DatabaseTestCase
from db_interface.models.word_list import WordList



class TestTeacher(DatabaseTestCase):
    def test_init(self):
        email = 'email@email.com'
        password = 'password'
        teacher = Teacher(password=password, email=email)
        self.assertEqual(teacher.email, email)
        self.assertEqual(teacher.password, password)
        self.assertIsNone(teacher.current_word_list)

    def test_commit(self):
        teacher = Teacher(password='pw', email='email')
        self.session.add(teacher)
        self.session.commit()
        answer = self.session.query(Teacher).all()[0]
        self.assertEqual(answer, teacher)
        self.assertIsInstance(answer.teacher_id, int)

    def test_commit_with_bad_word_list_id_raises_error(self):
        teacher = Teacher(password='pw', email='email')
        teacher.current_word_list = 1
        self.session.add(teacher)
        self.assertRaises(IntegrityError, self.session.commit)

    # def test_commit_with_default_score(self):
    #     teacher = Teacher(password='pw', email='email')
    #     self.session.add(teacher)
    #     self.session.commit()
    #     answer = self.session.query(Teacher).all()[0]
    #     self.assertEqual(answer, teacher)
    #     self.assertEqual(answer.score, 0)
    #
    # def test_commit_with_default_email(self):
    #     teacher = Teacher(password='pw', score=1)
    #     self.session.add(teacher)
    #     self.session.commit()
    #     answer = self.session.query(Teacher).all()[0]
    #     self.assertEqual(answer, teacher)
    #     self.assertIsNone(answer.email)
    #
    # def test_email_unique_constraint(self):
    #     email = 'email@email.com'
    #     teacher = Teacher(password='a', email=email, score=1)
    #     same_teacher_name = Teacher(password='b', email=email, score=2)
    #     self.session.add_all([teacher, same_teacher_name])
    #     self.assertRaises(IntegrityError, self.session.commit)
    #
    # def test_email_unique_constraint_allows_multiple_None_values(self):
    #     password = 'a'
    #     score = 1
    #     teacher = Teacher(password=password, score=score)
    #     other_teacher = Teacher(password=password, score=score)
    #     self.session.add_all((teacher, other_teacher))
    #     teacher_list = self.session.query(Teacher).all()
    #     self.assertEqual(len(teacher_list), 2)
    #     self.assertNotEqual(teacher_list[0].teacher_id, teacher_list[1].teacher_id)
    #
    # def test_password_score_not_unique(self):
    #     password = 'pw'
    #     score = 100
    #     first = Teacher(password=password, email='a', score=score)
    #     second = Teacher(password=password, email='b', score=score)
    #     self.session.add_all([first, second])
    #     self.assertIsNone(self.session.commit())
    #
    # def test_email_nullable(self):
    #     teacher = Teacher(password='pw', email=None, score=0)
    #     self.session.add(teacher)
    #     self.assertIsNone(self.session.commit())
    #
    # def test_all_fields_but_email_not_nullable(self):
    #     class_ = Teacher
    #     keys = ('password', 'score')
    #     values = ('random', 398)
    #     self.assert_not_nullable(class_, keys, values)
    #
    # def test_get_json_teacher(self):
    #     email = 'email'
    #     password = 'pw'
    #     score = 10
    #
    #     teacher = Teacher(password, email, score)
    #     self.session.add(teacher)
    #     self.session.commit()
    #     expected = {
    #         'email': email,
    #         'score': score,
    #         'teacher_id': teacher.teacher_id
    #     }
    #     self.assertEqual(teacher.get_json(), expected)
#
#