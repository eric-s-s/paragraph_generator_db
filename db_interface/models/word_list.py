from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from db_interface.models.base import Base


class WordList(Base):
    __tablename__ = 'word_list'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(30), nullable=False)
    document_data = Column(JSONB(none_as_null=True), nullable=False)

    UniqueConstraint(user_id, name)

