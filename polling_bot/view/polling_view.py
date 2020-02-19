from polling_bot.db.persist.polling_name_repo import PollingNameRepo
from polling_bot.excelquestions import ExcelQuestions
from polling_bot.view.sender import Sender
from telegram import ReplyKeyboardMarkup
import numpy as np

from polling_bot.state_machine.states import States
from polling_bot.view.constant_messages import Buttons
from polling_bot.view.sender import Sender


class PollingView:

    finish_poll_text = "شما با موفقیت نظرسنجی را به پایان رساندید\nبا تشکر از همراهی شما"

    def __init__(self, bot):
        self.sender = Sender(bot)

    def ask_question(self, user_id, q_number):
        question = ExcelQuestions()
        question_list = question.get_question_list()
        text = question_list[q_number][0]
        keyboard = []
        for q in question.get_question_answer(q_number):
            if isinstance(q, str):
                keyboard.append(q)

        if len(keyboard) > 0:
            reply_keyboard = [keyboard]
        else:
            keyboard.append('گزینه بعدی')
            reply_keyboard = [keyboard]
        # reply_keyboard = [Buttons.q_options]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard)
        self.sender.send_message(user_id, text, reply_markup=reply_markup)

    def finish_poll(self, user_id):
        text = self.finish_poll_text
        reply_keyboard = [[Buttons.polling]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard)
        self.sender.send_message(user_id, text, reply_markup=reply_markup)

    def show_start_message(self, user_id):
        text = PollingNameRepo.get_last_polling_message()
        if not text:
            text = "مشتری گرامی در حال حاظر هیچ نظرسنجی برای شما فعال نشده است."
        reply_keyboard = [[Buttons.continue_polling]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard)
        self.sender.send_message(user_id, text, reply_markup=reply_markup)
