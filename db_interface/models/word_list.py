from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB

from db_interface.models.base import Base


class WordList(Base):
    __tablename__ = 'word_list'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(30))
    json_list = Column(JSONB)

