# In the name of God
from sqlalchemy import Column, Integer, Boolean


from polling_bot.db.base import Base


class PollingControl(Base):
    __tablename__ = "polling_control"
    id = Column(Integer, autoincrement=True, primary_key=True)
    allowed = Column(Boolean, default=True, unique=True)

    def __init__(self, allowed):
        self.allowed = allowed
