import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_interface.verb import Base

TEST_DATA_BASE = 'postgresql+psycopg2://postgres:pw@172.17.0.2/paragraph_generator_test'
SQLITE_DATA_BASE = 'sqlite://'


class ModelTestBase(unittest.TestCase):
    base = None
    test_engine = None
    can_use_sqlite = False

    @classmethod
    def setUpClass(cls):
        data_base_connection_str = TEST_DATA_BASE
        if cls.can_use_sqlite:
            data_base_connection_str = SQLITE_DATA_BASE
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
