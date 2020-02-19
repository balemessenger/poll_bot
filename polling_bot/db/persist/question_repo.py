from loguru import logger

from polling_bot.db.base import session
from polling_bot.db.model.question import Question
from polling_bot.excelquestions import ExcelQuestions
from utils import db_persist
from sqlalchemy import func, desc
import pandas as pd


class QuestionRepo:

    @staticmethod
    def add(peer_id, question_number, answer, polling_name):
        try:
            question = Question(
                peer_id,
                question_number=question_number,
                polling_name=polling_name,
                answer=answer,
                flag=1
            )
            session.add(question)
            session.commit()
            logger.info("Added a question answer.")
            return question
        except Exception as e:
            session.rollback()
            logger.error("Failed to add question answer, error is {}".format(e))

    @staticmethod
    @db_persist(logger=logger)
    def exists_answer(peer_id,question_number):
        return session.query(session.query(Question).filter(Question.peer_id == peer_id).filter(Question.question_number==str(question_number)).exists()).scalar()

    @staticmethod
    @db_persist(logger=logger)
    def number_of_answered_questions(peer_id, question_number):
        return session.query(Question.answered_question_flag)\
            .filter(Question.answered_question_flag == 1).filter(Question.peer_id == peer_id).filter(Question.question_number == str(question_number - 1)).first()



    @staticmethod
    @db_persist(logger=logger)
    def update_flag():

        session.query(Question).filter(Question.answered_question_flag == 1).update({Question.answered_question_flag: 0})
        session.commit()

    @staticmethod
    def get_all_questions(polling_name):
        try:
            return session.query(Question).filter(Question.polling_name == polling_name)\
                .order_by(Question.peer_id, Question.question_number).all()

        except Exception as e:
            session.rollback()
            logger.error("Failed to get questions, {}".format(e))

    @staticmethod
    def get_all_participate(polling_name,question_number):
        try:
            return session.query(Question.peer_id).filter(Question.polling_name == polling_name)\
                .filter(Question.question_number == str(question_number)).distinct()

        except Exception as e:
            session.rollback()
            logger.error("Failed to get questions, {}".format(e))

    @staticmethod
    def get_question_answer(peer_id, question_number,polling_name):
        try:
            return session.query(Question.answer).filter(Question.polling_name == polling_name)\
                .filter(Question.question_number == str(question_number)).filter(Question.peer_id == peer_id).first()[0]

        except Exception as e:
            session.rollback()
            logger.error("Failed to get questions, {}".format(e))

    @staticmethod
    def get_question_number(last_polling_name):

        try:
            question_array =  session.query(Question.question_number).filter(Question.polling_name == last_polling_name)\
                .distinct()
            question_array = [int(item[0]) for item in question_array]
            return max(question_array)
        except Exception as e:
            session.rollback()
            logger.error("Failed to get questions, {}".format(e))


