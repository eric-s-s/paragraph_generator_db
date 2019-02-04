from sqlalchemy.exc import IntegrityError

from db_interface.models.nouns import CountableNoun, UncountableNoun, StaticNoun
from tests.models.model_test_base import ModelTestBase


class TestCountableNoun(ModelTestBase):
    can_use_sqlite = True

    def test_countable_noun_irregular_plural(self):
        noun = CountableNoun(value='child', irregular_plural='children')
        self.session.add(noun)
        self.session.commit()
        to_test = self.session.query(CountableNoun).all()[0]
        self.assertEqual(to_test.value, 'child')
        self.assertEqual(to_test.irregular_plural, 'children')
        self.assertIsInstance(to_test.id, int)

    def test_countable_noun_not_nullable_value(self):
        noun = CountableNoun(irregular_plural='x')
        self.session.add(noun)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_countable_noun_not_nullable_irregular_plural(self):
        noun = CountableNoun(value='x')
        self.session.add(noun)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_countable_noun_unique_value_constraint(self):
        noun = CountableNoun(value='x', irregular_plural='y')
        same_value = CountableNoun(value='x', irregular_plural='z')
        self.session.add_all((noun, same_value))
        self.assertRaises(IntegrityError, self.session.commit)


class TestUncountableNoun(ModelTestBase):
    can_use_sqlite = True

    def test_uncountable_noun_definite(self):
        noun = UncountableNoun(value='water')
        self.session.add(noun)
        self.session.commit()
        to_test = self.session.query(UncountableNoun).all()[0]
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


class TestStaticNoun(ModelTestBase):
    can_use_sqlite = True

    def test_static_noun_definite(self):
        noun = StaticNoun(value='Joe', is_plural=False)
        self.session.add(noun)
        self.session.commit()
        to_test = self.session.query(StaticNoun).all()[0]
        self.assertEqual(to_test.value, 'Joe')
        self.assertFalse(to_test.is_plural)
        self.assertIsInstance(to_test.id, int)

    def test_static_noun_not_nullable_value(self):
        noun = StaticNoun(is_plural=True)
        self.session.add(noun)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_static_noun_not_nullable_is_plural(self):
        noun = StaticNoun(value='Joe')
        self.session.add(noun)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_static_noun_unique_value_constraint(self):
        noun = StaticNoun(value='x', is_plural=True)
        same_value = StaticNoun(value='x', is_plural=False)
        self.session.add_all((noun, same_value))
        self.assertRaises(IntegrityError, self.session.commit)

