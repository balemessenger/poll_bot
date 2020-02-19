from sqlalchemy import Column, Integer, String

from polling_bot.db.base import Base


class User(Base):
    __tablename__ = "users"
    peer_id = Column(Integer, primary_key=True)
    age = Column(String)
    field = Column(String)
    experience_duration = Column(String)

    def __init__(self, peer_id: int, age: str, field: str, experience_duration: str):
        self.peer_id = peer_id
        self.age = age
        self.field = field
        self.experience_duration = experience_duration
