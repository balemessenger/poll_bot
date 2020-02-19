from loguru import logger

from polling_bot.db.base import session
from polling_bot.db.model.polling_control import PollingControl
from polling_bot.excelquestions import ExcelQuestions as q


class PollingControlRepo:

    @staticmethod
    def add_or_update(allowed):
        try:
            control = session.query(PollingControl).one_or_none()
            if not control:

                polling_control = PollingControl(
                    allowed=allowed
                )
                session.add(polling_control)
                session.commit()
            else:
                control.allowed = True
                session.commit()
                logger.info("Added a question answer.")

            return control

        except Exception as e:
            session.rollback()
            logger.error("Failed to add question answer, error is {}".format(e))

    @staticmethod
    def update_allowed():

        try:
            control = session.query(PollingControl).one_or_none()
            control.allowed = False
            session.commit()
            return control

        except Exception as e:
            session.rollback()
            logger.error("Faile to update polling controll, e:{}".format(e))

    @staticmethod
    def get_polling_control():

        try:
            control = session.query(PollingControl).one_or_none()
            return control.allowed
        except Exception as e:
            session.rollback()
            logger.error("Fail to get polling control, e:{}".format(e))
