from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Verb(Base):
    __tablename__ = 'verb'

    id = Column(Integer, primary_key=True)

    value = Column(String(30), nullable=False)
    irregular_past = Column(String(30), nullable=True)
    UniqueConstraint(value, irregular_past, name='a_name')

