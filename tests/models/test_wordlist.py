from itertools import chain

from db_interface.models.nouns import UncountableNoun, CountableNoun, StaticNoun
from db_interface.models.user import User, UserType
from db_interface.models.verb import Verb
from db_interface.models.word import Word, Tag
from db_interface.models.word_list import WordList
from tests.models.model_test_base import ModelTestBase


class TestWordList(ModelTestBase):

    def setUp(self):
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

        self.session.add_all(chain(self.words, self.verbs, self.countable_nouns, self.uncountable_nouns,
                                   self.static_nouns))
        self.session.commit()

    def test_thing(self):
        word_list_json = {
            'verbs': [{'verb': self.go.id, 'particle': 'away', 'preposition': '', 'objects': 0},
                      {'verb': self.play.id, 'particle': '', 'preposition': 'with', 'objects': 1}],
            'countable_nouns': [noun.id for noun in self.countable_nouns],
            'uncountable_nouns': [noun.id for noun in self.uncountable_nouns],
            'static_nouns': [noun.id for noun in self.static_nouns]
        }

        test_user = User(user_name='a', user_type=UserType.TEACHER)
        self.session.add(test_user)
        self.session.commit()

        word_list = WordList(user_id=test_user.id, name='list_name', json_list=word_list_json)

        self.session.add(word_list)
        self.session.commit()
        # expected = self.session.query(Word).filter(Word.value == 'away')[0]
        # self.assertEqual(expected.value, 'away')
        # self.assertEqual(expected.tag, Tag.PARTICLE)
        # print(expected.id)
        # print(self.away.id)
