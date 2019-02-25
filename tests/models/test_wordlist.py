from datetime import datetime
from itertools import chain

from sqlalchemy.exc import IntegrityError

from db_interface.models.nouns import UncountableNoun, CountableNoun, StaticNoun
from db_interface.models.teacher import Teacher
from db_interface.models.verb import Verb
from db_interface.models.word import Word, Tag
from db_interface.models.word_list import WordList
from tests.database_test_case import DatabaseTestCase


class TestWordList(DatabaseTestCase):

    def setUp(self):
        # TODO delete all but user
        super(TestWordList, self).setUp()
        self.with_ = Word(value='with', tag=Tag.PREPOSITION)
        self.away = Word(value='away', tag=Tag.PARTICLE)

        self.go = Verb(value='go', irregular_past='went')
        self.play = Verb(value='play')

        self.water = UncountableNoun(value='water')
        self.air = UncountableNoun(value='air')

        self.dog = CountableNoun(value='dog')
        self.child = CountableNoun(value='child', irregular_plural='children')

        self.joe = StaticNoun(value='Joe', is_plural=False)
        self.herbs = StaticNoun(value='Herbs', is_plural=True)

        self.words = [self.with_, self.away]
        self.verbs = [self.go, self.play]
        self.countable_nouns = [self.dog, self.child]
        self.uncountable_nouns = [self.water, self.air]
        self.static_nouns = [self.joe, self.herbs]

        self.test_teacher = Teacher(password='pw', email='email')

        self.session.add(self.test_teacher)
        self.session.commit()
        self.session.add_all(chain(self.words, self.verbs, self.countable_nouns, self.uncountable_nouns,
                                   self.static_nouns))
        self.session.commit()

    def test_init(self):
        teacher_id = 1
        name_ = 'x'
        document = {}
        now = datetime.now()
        word_list = WordList(teacher_id=teacher_id, name=name_, document_data=document, selection_timestamp=now)
        self.assertEqual(word_list.teacher_id, teacher_id)
        self.assertEqual(word_list.name, name_)
        self.assertEqual(word_list.document_data, document)
        self.assertEqual(word_list.selection_timestamp, now)

    def test_commit(self):
        teacher_id = self.test_teacher.teacher_id
        name_ = 'x'
        document = {}
        now = datetime.now()
        self.session.add(WordList(teacher_id=teacher_id, name=name_, document_data=document, selection_timestamp=now))
        self.session.commit()
        retrieved = self.session.query(WordList).first()
        self.assertEqual(retrieved.teacher_id, teacher_id)
        self.assertEqual(retrieved.name, name_)
        self.assertEqual(retrieved.document_data, document)
        self.assertEqual(retrieved.selection_timestamp, now)
        self.assertIsInstance(retrieved.teacher_id, int)

    def test_foreign_key_constraint(self):
        does_not_exist = self.test_teacher.teacher_id + 1
        name_ = 'x'
        document = {}
        self.session.add(WordList(teacher_id=does_not_exist, name=name_, document_data=document))
        self.assertRaises(IntegrityError, self.session.commit)

    def test_foreign_key_on_delete(self):
        teacher_id = self.test_teacher.teacher_id
        name_ = 'x'
        document = {}
        self.session.add(WordList(teacher_id=teacher_id, name=name_, document_data=document))
        self.session.commit()

        self.session.delete(self.test_teacher)
        self.session.commit()

        retrieved = self.session.query(WordList).all()
        self.assertEqual(retrieved, [])

    def test_unique_constraint_on_teacher_id_and_name(self):
        other_teacher = Teacher(email='other_teacher', password='pw')
        self.session.add(other_teacher)
        self.session.commit()

        document = {}

        name_ = 'a'
        other_name = 'b'

        word_list = WordList(name=name_, teacher_id=self.test_teacher.teacher_id, document_data=document)
        different_by_name = WordList(name=other_name, teacher_id=self.test_teacher.teacher_id, document_data=document)
        different_by_user = WordList(name=name_, teacher_id=other_teacher.teacher_id, document_data=document)
        self.session.add_all((word_list, different_by_name, different_by_user))
        self.assertIsNone(self.session.commit())

    def test_unique_constraint_raises_integrity_error(self):
        name_ = 'a'
        word_list = WordList(name=name_, teacher_id=self.test_teacher.teacher_id, document_data={})
        other_word_list = WordList(name=name_, teacher_id=self.test_teacher.teacher_id, document_data={'a': 1})
        self.session.add_all((word_list, other_word_list))
        self.assertRaises(IntegrityError, self.session.commit)

    def test_test_document_can_contain_int_str_list_dict_None(self):
        teacher_id = self.test_teacher.teacher_id
        name_ = 'x'
        document = {'a': None, 'b': 1, 'c': 'a string', 'd': [], 'e': {}}
        self.session.add(WordList(teacher_id=teacher_id, name=name_, document_data=document))
        self.session.commit()

        retrieved = self.session.query(WordList).first()
        self.assertEqual(retrieved.document_data, document)

    # TODO delete this test. it is just for demo
    def test_init_and_commit_this_is_a_bad_test_it_tests_many_things(self):
        word_list_document_data = {
            'verbs': [{'verb': self.go.id, 'particle': self.away.id, 'preposition': None, 'objects': 0},
                      {'verb': self.play.id, 'particle': None, 'preposition': self.away.id, 'objects': 1}],
            'countable_nouns': [noun.id for noun in self.countable_nouns],
            'uncountable_nouns': [noun.id for noun in self.uncountable_nouns],
            'static_nouns': [noun.id for noun in self.static_nouns]
        }
        word_list_name = 'list_name'

        self.session.add(self.test_teacher)
        self.session.commit()

        word_list = WordList(teacher_id=self.test_teacher.teacher_id, name=word_list_name,
                             document_data=word_list_document_data)

        self.session.add(word_list)
        self.session.commit()

        filter_ = WordList.teacher_id == self.test_teacher.teacher_id and WordList.name == word_list_name
        retrieved = self.session.query(WordList).filter(filter_)[0]  # type: WordList

        self.assertEqual(retrieved.document_data, word_list_document_data)
        self.assertEqual(retrieved.teacher_id, self.test_teacher.teacher_id)
        self.assertEqual(retrieved.name, word_list_name)
        self.assertIsInstance(retrieved.teacher_id, int)

    def test_not_nullable_fields(self):
        class_ = WordList
        keys = ('teacher_id', 'name', 'document_data')
        values = (self.test_teacher.teacher_id, 'joe', {'a': 'b'})
        self.assert_not_nullable(class_, keys, values)

    def test_selection_timestamp_is_nullable(self):
        teacher_id = self.test_teacher.teacher_id
        name_ = 'x'
        document = {}
        self.session.add(WordList(teacher_id=teacher_id, name=name_, document_data=document))
        self.session.commit()
        retrieved = self.session.query(WordList).first()
        self.assertIsNone(retrieved.selection_timestamp)

    def test_index_created_for_teacher_selection(self):
        expected = self.base.metadata.tables['word_list'].indexes.copy().pop()
        self.assertEqual(expected.name, 'teacher_selection')
        column_names = sorted(expected.columns.keys())
        self.assertEqual(column_names, ['selection_timestamp', 'teacher_id'])
