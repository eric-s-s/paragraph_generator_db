from sqlalchemy.exc import IntegrityError

from db_interface.models.word import Word, Tag
from tests.models.model_test_base import ModelTestBase


class TestWord(ModelTestBase):
    can_use_sqlite = True

    def test_Tag(self):
        self.assertEqual(Tag.PREPOSITION.value, 'PREPOSITION')
        self.assertEqual(Tag.PARTICLE.value, 'PARTICLE')

    def test_init(self):
        word = Word(value='with', tag='PREPOSITION')
        self.assertEqual(word.value, 'with')
        self.assertEqual(word.tag, 'PREPOSITION')

    def test_commit(self):
        word = Word(value='with', tag='PREPOSITION')
        self.session.add(word)
        self.session.commit()

        new_word = self.session.query(Word).all()[0]

        self.assertEqual(new_word.value, 'with')
        self.assertEqual(new_word.tag, Tag.PREPOSITION)
        self.assertIsInstance(new_word.id, int)

    def test_commit_word_not_in_enum(self):
        word = Word(value='which', tag='oops')
        self.session.add(word)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_enum_values(self):
        for enum_name in ('PREPOSITION', 'PARTICLE'):
            word = Word(value='a', tag=enum_name)
            self.session.add(word)
            self.session.commit()
            to_test = self.session.query(Word).filter(Word.tag == enum_name)[0]
            self.assertEqual(to_test.tag, getattr(Tag, enum_name))

    def test_unique_constraint_on_word_and_tag(self):
        word = Word(value='x', tag='PREPOSITION')
        different_by_tag = Word(value='x', tag='PARTICLE')
        different_by_value = Word(value='y', tag='PREPOSITION')
        self.session.add(word)
        self.session.add(different_by_tag)
        self.session.add(different_by_value)
        self.assertIsNone(self.session.commit())

    def test_unique_constraint_raises_integrity_error(self):
        word = Word(value='x', tag='PREPOSITION')
        same_word = Word(value='x', tag='PREPOSITION')
        self.session.add(word)
        self.session.add(same_word)
        self.assertRaises(IntegrityError, self.session.commit)

