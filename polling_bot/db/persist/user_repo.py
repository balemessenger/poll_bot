# In the name of God
from loguru import logger

from polling_bot.db.base import session
from polling_bot.db.model.user import User
from utils import db_persist


class UserRepo:

    @staticmethod
    def add(peer_id, age, field, experience_duration):
        try:
            user = User(peer_id, age, field, experience_duration)
            session.add(user)
            session.commit()
            logger.info("Added a user.")
            return user
        except Exception as e:
            session.rollback()
            logger.error("Failed to add user, error is {}".format(e))

    @staticmethod
    @db_persist(logger=logger)
    def exists(peer_id):
        return session.query(session.query(User).filter(User.peer_id == peer_id).exists()).scalar()

    @staticmethod
    @db_persist(logger=logger)
    def find_all():
        return session.query(User).all()
