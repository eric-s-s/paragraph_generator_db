import unittest

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from db_interface.models.base import Base

TEST_DATA_BASE = 'postgresql+psycopg2://postgres:pw@172.17.0.2/paragraph_generator_test'
SQLITE_DATA_BASE = 'sqlite://'


class DatabaseTestCase(unittest.TestCase):
    base = None
    test_engine = None

    @classmethod
    def setUpClass(cls):
        data_base_connection_str = TEST_DATA_BASE
        cls.test_engine = create_engine(data_base_connection_str)

        cls.base = Base
        cls.base.metadata.create_all(cls.test_engine)
        cls.TestSession = sessionmaker(cls.test_engine)

    @classmethod
    def tearDownClass(cls):
        cls.base.metadata.drop_all(cls.test_engine)

    def setUp(self):
        self.session = self.TestSession()
        self.clear_tables()

    def clear_tables(self):
        for table in Base.metadata.sorted_tables:
            self.session.execute(table.delete())

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def assert_not_nullable(self, class_, keys, values):
        for key in keys:
            kwargs = dict(zip(keys, values))
            kwargs[key] = None
            obj = class_(**kwargs)
            self.session.add(obj)
            self.assertRaises(IntegrityError, self.session.commit)
            self.session.rollback()
