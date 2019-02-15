from sqlalchemy.exc import IntegrityError

from db_interface.models.verb import Verb
from tests.models.model_test_base import ModelTestBase


class TestVerb(ModelTestBase):
    can_use_sqlite = True

    def test_create_verb_no_irregular_past(self):
        verb = Verb(value='play', irregular_past='')
        self.assertEqual(verb.value, 'play')
        self.assertEqual(verb.irregular_past, '')

    def test_create_verb_irregular_past_defaults_to_empty_str(self):
        verb = Verb(value='play')
        self.assertEqual(verb.irregular_past, '')

    def test_create_verb_no_irregular_past_commit(self):
        verb = Verb(value='play')
        self.session.add(verb)
        self.session.commit()
        answer = self.session.query(Verb).all()[0]
        self.assertEqual(verb, answer)
        self.assertIsInstance(verb.id, int)
        self.assertEqual(verb.irregular_past, '')

    def test_create_verb_irregular_past(self):
        verb = Verb(value='go', irregular_past='went')
        self.assertEqual(verb.value, 'go')
        self.assertEqual(verb.irregular_past, 'went')

    def test_create_verb_irregular_past_commit(self):
        verb = Verb(value='go', irregular_past='went')
        self.session.add(verb)
        self.session.commit()
        answer = self.session.query(Verb).all()[0]
        self.assertEqual(answer, verb)
        self.assertIsInstance(verb.id, int)

    def test_create_verb_does_not_raise_error_when_past_tense_not_the_same(self):
        first = Verb(value='hang', irregular_past='hung')
        second = Verb(value='hang', irregular_past='hanged')
        self.session.add(first)
        self.session.add(second)
        self.assertIsNone(self.session.commit())

    def test_create_verb_raises_error_over_non_unique_values(self):
        first = Verb(value='go', irregular_past='went')
        second = Verb(value='go', irregular_past='went')
        self.session.add(first)
        self.session.add(second)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_create_verb_raises_error_over_non_unique_values_when_irregular_past_is_empty_str(self):
        first = Verb(value='go', irregular_past='')
        second = Verb(value='go', irregular_past='')
        self.session.add(first)
        self.session.add(second)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_all_fields_not_nullable(self):
        class_ = Verb
        keys = ('value', 'irregular_past')
        values = ('a', 'b')
        self.assert_not_nullable(class_, keys, values)
