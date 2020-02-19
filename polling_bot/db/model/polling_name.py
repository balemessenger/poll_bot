# In the name of God
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import datetime

from polling_bot.db.base import Base


class PollingName(Base):
    __tablename__ = "polling_name"
    id = Column(Integer,autoincrement=True,primary_key=True)
    polling_name = Column(String)
    polling_message = Column(String)
    time = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, polling_name, polling_message):
        self.polling_message = polling_message
        self.polling_name = polling_name
        self.time = datetime.datetime.now()
