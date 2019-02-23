from sqlalchemy.exc import IntegrityError, DataError

from db_interface.models.word import Word, Tag
from tests.database_test_case import DatabaseTestCase


class TestWord(DatabaseTestCase):
    def test_Tag(self):
        self.assertEqual(getattr(Tag, 'PREPOSITION'), Tag.PREPOSITION)
        self.assertEqual(getattr(Tag, 'PARTICLE'), Tag.PARTICLE)
        self.assertEqual(len(Tag.__members__), 2)

    def test_init(self):
        word = Word(value='with', tag=Tag.PREPOSITION)
        self.assertEqual(word.value, 'with')
        self.assertEqual(word.tag, Tag.PREPOSITION)

    def test_commit(self):
        word = Word(value='with', tag=Tag.PREPOSITION)
        self.session.add(word)
        self.session.commit()

        new_word = self.session.query(Word).all()[0]

        self.assertEqual(new_word.value, 'with')
        self.assertEqual(new_word.tag, Tag.PREPOSITION)
        self.assertIsInstance(new_word.id, int)

    def test_commit_word_not_in_enum(self):
        word = Word(value='which', tag='oops')
        self.session.add(word)
        self.assertRaises(DataError, self.session.commit)

    def test_enum_values(self):
        for enum_name in (Tag.PREPOSITION, Tag.PARTICLE):
            word = Word(value='a', tag=enum_name)
            self.session.add(word)
            self.session.commit()
            to_test = self.session.query(Word).filter(Word.tag == enum_name)[0]
            self.assertEqual(to_test.tag, enum_name)

    def test_unique_constraint_on_word_and_tag(self):
        word = Word(value='x', tag=Tag.PREPOSITION)
        different_by_tag = Word(value='x', tag=Tag.PARTICLE)
        different_by_value = Word(value='y', tag=Tag.PREPOSITION)
        self.session.add(word)
        self.session.add(different_by_tag)
        self.session.add(different_by_value)
        self.assertIsNone(self.session.commit())

    def test_unique_constraint_raises_integrity_error(self):
        word = Word(value='x', tag=Tag.PREPOSITION)
        same_word = Word(value='x', tag=Tag.PREPOSITION)
        self.session.add(word)
        self.session.add(same_word)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_value_and_tag_not_nullable(self):
        class_ = Word
        keys = ('value', 'tag')
        values = ('x', Tag.PARTICLE)
        self.assert_not_nullable(class_, keys, values)

