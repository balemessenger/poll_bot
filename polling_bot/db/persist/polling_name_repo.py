from loguru import logger

from polling_bot.db.base import session
from polling_bot.db.model.polling_name import PollingName
from utils import db_persist
from sqlalchemy import func


class PollingNameRepo:

    @staticmethod
    def add(polling_name, polling_message):
        try:
            polling = PollingName(
                polling_name=polling_name,
                polling_message=polling_message
            )
            session.add(polling)
            session.commit()
            logger.info("Added a question answer.")
            return polling_name
        except Exception as e:
            session.rollback()
            logger.error("Failed to add question answer, error is {}".format(e))

    @staticmethod
    def get_polling_name(polling_number):
        try:
            all_polling_names = session.query(PollingName).order_by(PollingName.time).all()
            return all_polling_names[polling_number].polling_name

        except Exception as e:
            session.rollback()
            logger.error("Failed get polling name, error:{}".format(e))

    @staticmethod
    def get_last_polling_message():
        try:
            all_polling_messages = session.query(PollingName).order_by(PollingName.time).all()
            if len(all_polling_messages) > 0:
                return all_polling_messages[-1].polling_message
            else:
                return None

        except Exception as e:
            session.rollback()
            logger.error("Failed to get polling message")

