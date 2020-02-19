import os

import sys
from loguru import logger
from telegram import Update
from telegram.ext import Dispatcher, ConversationHandler

from polling_bot import MAIN_DIRECTORY
from polling_bot.config import Config
from polling_bot.db.persist.polling_controll_repo import PollingControlRepo
from polling_bot.db.persist.polling_name_repo import PollingNameRepo
from polling_bot.view.constant_messages import Buttons
from result_writer import ResultWriter
from ..db.persist.question_repo import QuestionRepo
from ..db.persist.user_repo import UserRepo
from ..excelquestions import ExcelQuestions
from ..state_machine.states import States
from ..view.polling_view import PollingView


RESULT_PATH = os.path.join(MAIN_DIRECTORY, 'data')
counter = 0


class PollingController:
    finish_poll = "شما با موفقیت نظرسنجی را به پایان رساندید\nبا تشکر از همراهی شما"

    def __init__(self, dispatcher: Dispatcher):
        self.view = PollingView(dispatcher.bot)
        self.dispatcher = dispatcher
        self.current_polling = -1

    def ask_question(self, bot, update: Update):
        user_id = update.effective_user.id
        question_list = ExcelQuestions().get_question_list()
        replace_is_answered = QuestionRepo.number_of_answered_questions(user_id, len(question_list))
        allowed = PollingControlRepo.get_polling_control()
        if replace_is_answered or not allowed:
            self.view.finish_poll(user_id)
            return ConversationHandler.END

        self.view.show_start_message(user_id)
        return States.SHOW_QUESTIONS

    def show_questions(self, bot, update):
        user_id = update.effective_user.id
        question_list = ExcelQuestions().get_question_list()
        message = update.message.text
        allowed = PollingControlRepo.get_polling_control()
        replace_is_answered = QuestionRepo.number_of_answered_questions(user_id, len(question_list))
        if replace_is_answered or (not allowed and message == Buttons.show_polling_questions):
            self.view.finish_poll(user_id)
            return ConversationHandler.END

        user_id = update.effective_user.id
        text = update.message.text
        q = ExcelQuestions()

        polling_name = PollingNameRepo.get_polling_name(self.current_polling)

        print(self.dispatcher.user_data.get("q_number"+str(user_id)))
        if str(self.dispatcher.user_data.get("q_number"+str(user_id))).isdigit():
            question_number = self.dispatcher.user_data.get("q_number"+str(user_id))
            answer_list = q.get_question_answer(question_number)
            answer_list = [str(item).strip() for item in answer_list]
            logger.error(answer_list)
            if text.strip() not in answer_list:
                answer_index = text
                logger.error(text)
            else:
                answer_index = str(answer_list.index(text.strip()) + 1)

            if self.dispatcher.user_data["q_number" + str(user_id)] >= len(question_list) - 1:
                QuestionRepo.add(
                    user_id,
                    question_number,
                    answer_index,
                    polling_name
                )
                self.view.finish_poll(user_id)
                self.dispatcher.user_data["q_number" + str(user_id)] = None
                return ConversationHandler.END
            QuestionRepo.add(
                user_id,
                question_number,
                answer_index,
                polling_name
            )
            print(self.dispatcher.user_data["q_number"+str(user_id)])
            self.dispatcher.user_data["q_number"+str(user_id)] += 1
        else:
            self.dispatcher.user_data["q_number"+str(user_id)] = 0
        self.view.ask_question(user_id,self.dispatcher.user_data["q_number"+str(user_id)])

        return States.QUESTION

    def save_document(self, bot, update):
        user = update.effective_user.id
        if not str(user) in Config.SUPPORTED_USERS:
            return

        file = bot.get_file(update.message.document.file_id)
        file.download(os.path.join(RESULT_PATH, 'polling.xlsx'))
        bot.send_message(chat_id=user, text='لطفا پیام آغازین این نظرسنجی را وارد کنید')
        QuestionRepo.update_flag()
        return States.POLLING_MESSAGE

    def get_polling_message(self, bot, update):
        chat_id = update.effective_user.id
        message = update.message.text
        self.dispatcher.user_data['polling_message'] = message
        bot.send_message(chat_id=chat_id, text="لطفا نام نظرسنجی را مشخص کنید")
        return States.POLLING_NAME

    def get_polling_name(self, bot, update):
        chat_id = update.effective_user.id
        polling_name = update.message.text
        PollingNameRepo.add(polling_name, polling_message=self.dispatcher.user_data['polling_message'])
        PollingControlRepo.add_or_update(True)
        bot.send_message(chat_id=chat_id, text="با تشکر، نظرسنجی مورد نظر ایجاد گردید.")
        os._exit(0)
        return ConversationHandler.END

    def get_report(self, bot, update):
        chat_id = update.effective_user.id
        message = update.message.text
        polling_number = int(message.split(",")[1])
        print(polling_number)

        logger.info("user {} Try to get report".format(chat_id))
        if not str(chat_id) in Config.SUPPORTED_USERS:
            return

        last_polling_name = PollingNameRepo.get_polling_name(polling_number)
        print(last_polling_name)
        question_number = QuestionRepo.get_question_number(last_polling_name)
        print(question_number)
        all_participate = QuestionRepo.get_all_participate(last_polling_name,int(question_number))
        logger.error(all_participate)
        question_answer_list = []
        for participant in all_participate:
            user_answer = [participant[0]]
            for question in range(question_number+1):
                answer = QuestionRepo.get_question_answer(participant[0],str(question),last_polling_name)
                logger.error(str(question)+"-"+str(answer))
                if answer is not None and answer != "":
                    user_answer+=[answer]
                else:
                    user_answer+=["بدون جواب"]
            question_answer_list += [user_answer]
        logger.error(question_answer_list)
        all_questions = QuestionRepo.get_all_questions(last_polling_name)
        logger.error(all_questions)
        result_writer = ResultWriter(os.path.join(RESULT_PATH, 'report.xlsx'))

        result_writer.write_to_excel(question_answer_list, 'report')
        bot.send_document(
            chat_id=chat_id,
            document=open(os.path.join(RESULT_PATH, 'report.xlsx'), 'rb')
        )
        logger.info("user {} gets the report".format(chat_id))

    def finish_polling(self, bot, update):
        chat_id = update.effective_user.id
        if not str(chat_id) in Config.SUPPORTED_USERS:
            return

        control = PollingControlRepo.update_allowed()
        assert control.allowed is False
        bot.send_message(chat_id=chat_id, text="نظر سنجی متوقف شد")









