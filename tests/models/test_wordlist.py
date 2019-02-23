from itertools import chain

from sqlalchemy.exc import IntegrityError

from db_interface.models.nouns import UncountableNoun, CountableNoun, StaticNoun
from db_interface.models.user import User, UserType
from db_interface.models.verb import Verb
from db_interface.models.word import Word, Tag
from db_interface.models.word_list import WordList
from tests.models.model_test_base import ModelTestBase


class TestWordList(ModelTestBase):

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

        self.test_user = User(user_name='a', user_type=UserType.TEACHER)

        self.session.add(self.test_user)
        self.session.commit()
        self.session.add_all(chain(self.words, self.verbs, self.countable_nouns, self.uncountable_nouns,
                                   self.static_nouns))
        self.session.commit()

    def test_init(self):
        user_id = 1
        name_ = 'x'
        document = {}
        word_list = WordList(user_id=user_id, name=name_, document_data=document)
        self.assertEqual(word_list.user_id, user_id)
        self.assertEqual(word_list.name, name_)
        self.assertEqual(word_list.document_data, document)

    def test_commit(self):
        user_id = self.test_user.id
        name_ = 'x'
        document = {}
        self.session.add(WordList(user_id=user_id, name=name_, document_data=document))
        self.session.commit()
        retrieved = self.session.query(WordList).all()[0]
        self.assertEqual(retrieved.user_id, user_id)
        self.assertEqual(retrieved.name, name_)
        self.assertEqual(retrieved.document_data, document)
        self.assertIsInstance(retrieved.id, int)

    def test_foreign_key_constraint(self):
        does_not_exist = self.test_user.id + 1
        name_ = 'x'
        document = {}
        self.session.add(WordList(user_id=does_not_exist, name=name_, document_data=document))
        self.assertRaises(IntegrityError, self.session.commit)

    def test_foreign_key_on_delete(self):
        user_id = self.test_user.id
        name_ = 'x'
        document = {}
        self.session.add(WordList(user_id=user_id, name=name_, document_data=document))
        self.session.commit()

        self.session.delete(self.test_user)

        retrieved = self.session.query(WordList).all()
        self.assertEqual(retrieved, [])

    def test_unique_constraint_on_user_id_and_name(self):
        other_user = User('other_user', UserType.TEACHER)
        self.session.add(other_user)
        self.session.commit()

        document = {}

        name_ = 'a'
        other_name = 'b'

        word_list = WordList(name=name_, user_id=self.test_user.id, document_data=document)
        different_by_name = WordList(name=other_name, user_id=self.test_user.id, document_data=document)
        different_by_user = WordList(name=name_, user_id=other_user.id, document_data=document)
        self.session.add_all((word_list, different_by_name, different_by_user))
        self.assertIsNone(self.session.commit())

    def test_unique_constraint_raises_integrity_error(self):
        name_ = 'a'
        word_list = WordList(name=name_, user_id=self.test_user.id, document_data={})
        other_word_list = WordList(name=name_, user_id=self.test_user.id, document_data={'a': 1})
        self.session.add_all((word_list, other_word_list))
        self.assertRaises(IntegrityError, self.session.commit)

    def test_test_document_can_contain_int_str_list_dict_None(self):
        user_id = self.test_user.id
        name_ = 'x'
        document = {'a': None, 'b': 1, 'c': 'a string', 'd': [], 'e': {}}
        self.session.add(WordList(user_id=user_id, name=name_, document_data=document))
        self.session.commit()

        retrieved = self.session.query(WordList).all()[0]
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

        self.session.add(self.test_user)
        self.session.commit()

        word_list = WordList(user_id=self.test_user.id, name=word_list_name, document_data=word_list_document_data)

        self.session.add(word_list)
        self.session.commit()

        filter_ = WordList.user_id == self.test_user.id and WordList.name == word_list_name
        retrieved = self.session.query(WordList).filter(filter_)[0]  # type: WordList

        self.assertEqual(retrieved.document_data, word_list_document_data)
        self.assertEqual(retrieved.user_id, self.test_user.id)
        self.assertEqual(retrieved.name, word_list_name)
        self.assertIsInstance(retrieved.id, int)

    def test_all_fields_not_nullable(self):
        class_ = WordList
        keys = ('user_id', 'name', 'document_data')
        values = (self.test_user.id, 'joe', {'a': 'b'})
        self.assert_not_nullable(class_, keys, values)
