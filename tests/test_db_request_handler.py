from db_interface.db_request_handler import DBRequestHandler, BadIdError, NotFoundError
from db_interface.models.nouns import CountableNoun, UncountableNoun, StaticNoun
from db_interface.models.student import Student
from db_interface.models.teacher import Teacher
from db_interface.models.verb import Verb
from db_interface.models.word import Word, Tag
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
        password = 'password'
        response_json = self.request_handler.create_teacher(password, email)
        expected = {
            'email': email,
            'teacher_id': response_json['teacher_id']
        }
        self.assertIsInstance(response_json['teacher_id'], int)
        self.assertEqual(response_json, expected)

        teacher = self.session.query(Teacher).first()
        self.assertEqual(teacher.get_json(), response_json)
        self.assertEqual(teacher.password, password)

    def test_create_student(self):
        email = 'a@b'
        password = 'a'
        score = 100
        response_json = self.request_handler.create_student(password=password, email=email, score=score)
        expected = {
            'email': email,
            'score': score,
            'student_id': response_json['student_id']
        }
        self.assertEqual(response_json, expected)
        self.assertIsInstance(response_json['student_id'], int)

        student = self.session.query(Student).first()
        self.assertEqual(student.get_json(), response_json)
        self.assertEqual(student.password, password)

    def test_create_student_no_score(self):
        email = 'email'
        password = 'pw'
        response_json = self.request_handler.create_student(password, email)
        expected = {
            'email': email,
            'score': 0,
            'student_id': response_json['student_id']
        }
        self.assertEqual(response_json, expected)

        student = self.session.query(Student).first()
        self.assertEqual(student.get_json(), response_json)
        self.assertEqual(student.password, password)

    def test_create_student_no_email(self):
        password = 'pw'
        score = 10
        response_json = self.request_handler.create_student(password=password, score=score)
        expected = {
            'email': None,
            'score': score,
            'student_id': response_json['student_id']
        }
        self.assertEqual(response_json, expected)

        student = self.session.query(Student).first()
        self.assertEqual(student.get_json(), response_json)
        self.assertEqual(student.password, password)

    def test_get_student_id(self):
        password = 'pw'
        email = 'email'
        response = self.request_handler.create_student(password, email)
        student_id = response['student_id']
        self.assertEqual(self.request_handler.get_student_id(email), student_id)

    def test_get_student_id_raises_NotFoundError(self):
        self.assertRaises(NotFoundError, self.request_handler.get_student_id, 'oops')

    def test_get_teacher_id(self):
        password = 'pw'
        email = 'email'
        response = self.request_handler.create_teacher(password, email)
        teacher_id = response['teacher_id']
        self.assertEqual(self.request_handler.get_teacher_id(email), teacher_id)

    def test_get_teacher_id_raises_NotFoundError(self):
        self.assertRaises(NotFoundError, self.request_handler.get_teacher_id, 'oops')

    def test_is_student_login_correct_true(self):
        password = 'pw'
        email = 'email'
        response = self.request_handler.create_student(password, email)
        id_ = response['student_id']
        self.assertTrue(self.request_handler.is_student_login_correct(id_, password))

    def test_is_student_login_correct_false(self):
        password = 'pw'
        email = 'email'
        response = self.request_handler.create_student(password, email)
        id_ = response['student_id']
        self.assertFalse(self.request_handler.is_student_login_correct(id_, password + 'oops'))

    def test_is_student_login_correct_raises_BadIdError(self):
        self.assertRaises(BadIdError, self.request_handler.is_student_login_correct, 1, 'pw')

    def test_is_teacher_login_correct_true(self):
        password = 'pw'
        email = 'email'
        response = self.request_handler.create_teacher(password, email)
        id_ = response['teacher_id']
        self.assertTrue(self.request_handler.is_teacher_login_correct(id_, password))

    def test_is_teacher_login_correct_false(self):
        password = 'pw'
        email = 'email'
        response = self.request_handler.create_teacher(password, email)
        id_ = response['teacher_id']
        self.assertFalse(self.request_handler.is_teacher_login_correct(id_, password + 'oops'))

    def test_is_teacher_login_correct_raises_BadIdError(self):
        self.assertRaises(BadIdError, self.request_handler.is_teacher_login_correct, 1, 'pw')

    def test_get_student(self):
        score = 10
        response = self.request_handler.create_student('pw', score=score)
        student_id = response['student_id']
        expected = {
            'email': None,
            'student_id': student_id,
            'score': score
        }

        actual = self.request_handler.get_student(student_id)
        self.assertEqual(expected, actual)

    def test_get_student_bad_id_raises_BadIdError(self):
        self.assertRaises(BadIdError, self.request_handler.get_student, 1)

    def test_get_teacher(self):
        email = 'email'
        response = self.request_handler.create_teacher('pw', email)
        teacher_id = response['teacher_id']
        expected = {
            'email': email,
            'teacher_id': teacher_id,
        }

        actual = self.request_handler.get_teacher(teacher_id)
        self.assertEqual(expected, actual)

    def test_get_teacher_bad_id_raises_BadIdError(self):
        self.assertRaises(BadIdError, self.request_handler.get_teacher, 1)

    def test_update_score_returns_correct_response(self):
        score = 10
        new_score = 20
        student_id = self.request_handler.create_student('pw', score=score)['student_id']
        expected = {
            'student_id': student_id,
            'email': None,
            'score': new_score
        }

        response = self.request_handler.update_score(student_id, new_score)
        self.assertEqual(expected, response)

    def test_update_score_updates_database(self):
        score = 10
        new_score = 20
        student_id = self.request_handler.create_student('pw', score=score)['student_id']
        expected = {
            'student_id': student_id,
            'email': None,
            'score': new_score
        }
        self.request_handler.update_score(student_id, new_score)

        is_updated = self.request_handler.get_student(student_id)
        self.assertEqual(expected, is_updated)

    def test_update_score_raises_BadIdError(self):
        self.assertRaises(BadIdError, self.request_handler.update_score, 1, 10)

    def test_create_preposition_response(self):
        preposition = 'away'
        response = self.request_handler.create_preposition(preposition)
        expected = {
            'value': preposition,
            'tag': 'PREPOSITION',
            'id': response['id']
        }
        self.assertEqual(response, expected)

    def test_create_preposition_in_database(self):
        preposition = 'away'
        response = self.request_handler.create_preposition(preposition)
        from_database = self.session.query(Word).first()
        self.assertEqual(response, from_database.get_json())

    def test_create_particle_response(self):
        particle = 'up'
        response = self.request_handler.create_particle(particle)
        expected = {
            'value': particle,
            'tag': 'PARTICLE',
            'id': response['id']
        }
        self.assertEqual(response, expected)

    def test_create_particle_in_database(self):
        particle = 'up'
        response = self.request_handler.create_particle(particle)
        from_database = self.session.query(Word).first()
        self.assertEqual(response, from_database.get_json())

    def test_create_verb_response(self):
        verb = 'go'
        irregular_past = 'went'
        response = self.request_handler.create_verb(verb, irregular_past)
        expected = {
            'value': verb,
            'irregular_past': irregular_past,
            'id': response['id']
        }
        self.assertEqual(response, expected)

    def test_create_verb_default_irregular_past(self):
        verb = 'play'
        response = self.request_handler.create_verb(verb)
        expected = {
            'value': verb,
            'irregular_past': '',
            'id': response['id']
        }
        self.assertEqual(expected, response)

    def test_create_verb_in_database(self):
        verb = 'child'
        irregular_past = 'children'
        response = self.request_handler.create_verb(verb, irregular_past)
        from_database = self.session.query(Verb).first()
        self.assertEqual(response, from_database.get_json())

    def test_create_countable_noun_response(self):
        noun = 'child'
        irregular_plural = 'children'
        response = self.request_handler.create_countable_noun(noun, irregular_plural)
        expected = {
            'value': noun,
            'irregular_plural': irregular_plural,
            'id': response['id']
        }
        self.assertEqual(response, expected)

    def test_create_countable_noun_default_irregular_plural(self):
        noun = 'dog'
        response = self.request_handler.create_countable_noun(noun)
        expected = {
            'value': 'dog',
            'irregular_plural': '',
            'id': response['id']
        }
        self.assertEqual(expected, response)

    def test_create_countable_noun_in_database(self):
        countable_noun = 'child'
        irregular_plural = 'children'
        response = self.request_handler.create_countable_noun(countable_noun, irregular_plural)
        from_database = self.session.query(CountableNoun).first()
        self.assertEqual(response, from_database.get_json())

    def test_create_uncountable_noun_response(self):
        noun = 'water'
        response = self.request_handler.create_uncountable_noun(noun)
        expected = {
            'value': noun,
            'id': response['id']
        }
        self.assertEqual(response, expected)

    def test_create_uncountable_noun_in_database(self):
        uncountable_noun = 'air'
        response = self.request_handler.create_uncountable_noun(uncountable_noun)
        from_database = self.session.query(UncountableNoun).first()
        self.assertEqual(response, from_database.get_json())

    def test_create_static_noun_response(self):
        noun = 'Joe'
        is_plural = False
        response = self.request_handler.create_static_noun(noun, is_plural)
        expected = {
            'value': noun,
            'id': response['id'],
            'is_plural': is_plural
        }
        self.assertEqual(expected, response)

    def test_create_static_noun_in_database(self):
        noun = 'Joe'
        is_plural = True
        response = self.request_handler.create_static_noun(noun, is_plural)
        from_database = self.session.query(StaticNoun).first()
        self.assertEqual(response, from_database.get_json())


    def test_get_all_static_nouns(self):
        pass

    def test_get_all_unstatic_nouns(self):
        pass

        pass

    def test_get_all_verbs(self):
        pass

    def test_get_preposition_or_particle(self):
        pass

    def test_get_static_noun(self):
        pass

    def test_get_unstatic_noun(self):
        pass


    def test_get_verb(self):
        pass

    def test_create_word_list(self):
        pass

    def test_get_word_list(self):
        pass

    def test_update_word_list(self):
        pass

    def test_get_word_lists_for_teacher(self):
        pass

    def test_update_current_word_list_selection_for_teacher(self):
        pass

    def test_get_current_word_list_selection_for_teacher(self):
        pass

    def test_get_all_prepositions_and_particles_no_entries(self):
        self.assertEqual(self.request_handler.get_all_prepositions_and_particles(), [])

    def test_get_prepositions_and_particles_with_entries(self):
        with_ = Word(value='with', tag=Tag.PREPOSITION)
        over = Word(value='over', tag=Tag.PREPOSITION)
        away = Word(value='away', tag=Tag.PARTICLE)
        self.session.add_all([with_, over, away])
        self.session.commit()
        expected = [word.get_json() for word in (with_, over, away)]
        expected.sort(key=lambda word: word['id'])

        actual = self.request_handler.get_all_prepositions_and_particles()
        actual.sort(key=lambda word: word['id'])

        self.assertEqual(expected, actual)
