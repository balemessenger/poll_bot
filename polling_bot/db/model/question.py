# In the name of God
from sqlalchemy import Column, Integer, String, DateTime
import datetime

from polling_bot.db.base import Base


class Question(Base):
    __tablename__ = "question"
    id = Column(Integer, autoincrement=True, primary_key=True)
    peer_id = Column(Integer)
    question_number = Column(String)
    answered_question_flag = Column(Integer)
    answer = Column(String)
    polling_name = Column(String)
    time = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, peer_id: int, question_number: str, answer: str, flag: int, polling_name: str):
        self.peer_id = peer_id
        self.question_number = question_number
        self.answer = answer
        self.answered_question_flag = flag
        self.polling_name = polling_name

