# In the name of God

from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton

from polling_bot.db.persist.polling_name_repo import PollingNameRepo
from polling_bot.state_machine.states import States
from polling_bot.view.constant_messages import Buttons
from polling_bot.view.sender import Sender


class MainView:
    start = ""

    polling_start = ""
   
    def __init__(self, bot: Bot):
        self.sender = Sender(bot)

    def send_registeration_menu(self, user_id):
        # text = self.start
        text = PollingNameRepo.get_last_polling_message()
        reply_keyboard = [[Buttons.register]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard)
        self.sender.send_message(user_id, text, reply_markup=reply_markup)

    def send_polling_menu(self, user_id):
        # text = self.start
        text = PollingNameRepo.get_last_polling_message()
        if not text:
            text = "مشتری گرامی در حال حاظر هیچ نظرسنجی برای شما فعال نشده است."
        reply_keyboard = [[Buttons.show_polling_questions]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard)
        self.sender.send_message(user_id, text, reply_markup=reply_markup)

