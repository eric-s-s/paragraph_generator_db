import unittest
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.exc import UnboundExecutionError

from db_interface.data_base_session import data_base_session_scope, DataBaseSession


class TestDataBaseSession(unittest.TestCase):

    def setUp(self):
        DataBaseSession.configure(bind=None)

    @patch('db_interface.data_base_session.DataBaseSession')
    def test_context_manager_closes_on_exit(self, mock_session):
        with data_base_session_scope() as session:
            pass
        session.close.assert_called_once()

    @patch('db_interface.data_base_session.DataBaseSession')
    def test_context_manager_closes_on_exit_with_error_raised(self, mock_session):
        session_instance = mock_session.return_value
        session_instance.thingy.side_effect = ValueError('nope')
        with self.assertRaises(ValueError):
            with data_base_session_scope() as session:
                session.thingy()
            session.close.assert_called_once()

    def test_setUp_DataBaseSession_unbound(self):
        with data_base_session_scope() as session:
            self.assertRaises(UnboundExecutionError, session.get_bind)

    def test_binding_to_DataBaseSession(self):
        in_memory = create_engine('sqlite://')
        DataBaseSession.configure(bind=in_memory)
        with data_base_session_scope() as session:
            engine = session.get_bind()
            self.assertIs(engine, in_memory)


