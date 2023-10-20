from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import func

from app.db_session import DBSession


Base = DBSession.Base()


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, unique=True, index=True)
    answer = Column(String)
    value = Column(Integer)
    airdate = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    category_id = Column(Integer)
    saved_at = Column(DateTime, server_default=func.now())
