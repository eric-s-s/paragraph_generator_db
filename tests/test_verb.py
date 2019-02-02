import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_interface.verb import Verb, Base

test_engine = create_engine('sqlite://')
TestSession = sessionmaker(test_engine)


Base.metadata.create_all(test_engine)


class TestVerb(unittest.TestCase):
    def setUp(self):
        self.session = TestSession()
        self.clear_tables()

    def clear_tables(self):
        for table in Base.metadata.sorted_tables:
            self.session.execute(table.delete())

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_create_verb_no_irregular_past(self):
        verb = Verb(value='play')
        self.assertEqual(verb.value, 'play')
        self.assertEqual(verb.irregular_past, None)

    def test_create_verb_no_irregular_past_commit(self):
        verb = Verb(value='play')
        self.session.add(verb)
        self.session.commit()
        answer = self.session.query(Verb).all()[0]
        self.assertEqual(verb, answer)
        self.assertIsInstance(verb.id, int)

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

    def test_create_verb_unique_over_two_keys(self):
        first = Verb(value='play')
        second = Verb(value='play')
        self.session.add(first)
        self.session.add(second)
        self.session.commit()
        for word in self.session.query(Verb).all():
            print(word.value, word.irregular_past)
        
