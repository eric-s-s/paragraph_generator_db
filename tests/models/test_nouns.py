from sqlalchemy.exc import IntegrityError

from db_interface.models.nouns import CountableNoun, UncountableNoun, StaticNoun
from tests.database_test_case import DatabaseTestCase


class TestCountableNoun(DatabaseTestCase):

    def test_countable_noun_irregular_plural(self):
        noun = CountableNoun(value='child', irregular_plural='children')
        self.session.add(noun)
        self.session.commit()
        to_test = self.session.query(CountableNoun).first()
        self.assertEqual(to_test.value, 'child')
        self.assertEqual(to_test.irregular_plural, 'children')
        self.assertIsInstance(to_test.id, int)

    def test_countable_noun_default_irregular_plural_is_empty_string(self):
        noun = CountableNoun(value='a')
        self.assertEqual(noun.irregular_plural, '')
        self.session.add(noun)
        self.session.commit()
        to_test = self.session.query(CountableNoun).first()
        self.assertEqual(noun, to_test)

    def test_countable_noun_not_nullable_value_and_irregular_plural(self):
        class_ = CountableNoun
        keys = ('value', 'irregular_plural')
        values = ('a', 'b')
        self.assert_not_nullable(class_, keys, values)

    def test_countable_noun_unique_value_constraint(self):
        noun = CountableNoun(value='x', irregular_plural='y')
        same_value = CountableNoun(value='x', irregular_plural='z')
        self.session.add_all((noun, same_value))
        self.assertRaises(IntegrityError, self.session.commit)


class TestUncountableNoun(DatabaseTestCase):
    def test_uncountable_noun_definite(self):
        noun = UncountableNoun(value='water')
        self.session.add(noun)
        self.session.commit()
        to_test = self.session.query(UncountableNoun).first()
        self.assertEqual(to_test.value, 'water')
        self.assertIsInstance(to_test.id, int)

    def test_uncountable_noun_not_nullable_value(self):
        noun = UncountableNoun()
        self.session.add(noun)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_uncountable_noun_unique_value_constraint(self):
        noun = UncountableNoun(value='x')
        same_value = UncountableNoun(value='x')
        self.session.add_all((noun, same_value))
        self.assertRaises(IntegrityError, self.session.commit)


class TestStaticNoun(DatabaseTestCase):
    def test_static_noun_definite(self):
        noun = StaticNoun(value='Joe', is_plural=False)
        self.session.add(noun)
        self.session.commit()
        to_test = self.session.query(StaticNoun).first()
        self.assertEqual(to_test.value, 'Joe')
        self.assertFalse(to_test.is_plural)
        self.assertIsInstance(to_test.id, int)

    def test_static_noun_not_nullable_value(self):
        noun = StaticNoun(is_plural=True)
        self.session.add(noun)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_static_noun_not_nullable_value_is_plural(self):
        class_ = StaticNoun
        keys = ('value', 'is_plural')
        values = ('a', True)
        self.assert_not_nullable(class_, keys, values)

    def test_static_noun_unique_value_constraint(self):
        noun = StaticNoun(value='x', is_plural=True)
        same_value = StaticNoun(value='x', is_plural=False)
        self.session.add_all((noun, same_value))
        self.assertRaises(IntegrityError, self.session.commit)
