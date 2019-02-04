from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_interface.models.verb import Verb, Base

"""
NOTE: DataBaseSession requires binding to an engine using DataBaseSession.configure(bind=some_engine)
"""
"""
postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]


"""
DataBaseSession = sessionmaker()


@contextmanager
def data_base_session_scope():
    session = DataBaseSession()
    try:
        yield session
    finally:
        session.close()


app_engine = create_engine(
    'postgresql+psycopg2://postgres:pw@172.17.0.2/paragraph_generator'

)

DataBaseSession.configure(bind=app_engine)

Base.metadata.create_all(app_engine)


with data_base_session_scope() as a_session:
    print(a_session)
    go = Verb(value='go', irregular_past='went')
    play = Verb(value='play')
    stupid_go = Verb(value='go')
    a_session.add(go)
    a_session.commit()

with data_base_session_scope() as a_session:
    print(a_session.query(Verb).all())
