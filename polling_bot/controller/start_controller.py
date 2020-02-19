# In the name of God
from loguru import logger
from telegram import Update
from telegram.ext import Dispatcher, ConversationHandler

from polling_bot.db.persist.user_repo import UserRepo
from polling_bot.state_machine.states import States
from utils import log_error
from polling_bot.view.start_view import MainView


class MainController:
    def __init__(self, dispatcher: Dispatcher):
        self.view = MainView(dispatcher.bot)
        self.dispatcher = dispatcher

    @log_error(logger)
    def main_menu(self, bot, update: Update):
        user_id = update.effective_user.id
        is_registered = UserRepo.exists(user_id)
        # if not is_registered:
        #     self.view.send_registeration_menu(user_id)
        #     return ConversationHandler.END
        # else:
        self.dispatcher.user_data["question_number"] = 1
        self.view.send_polling_menu(user_id)
        return ConversationHandler.END

    @log_error(logger)
    def ask_question (self, bot, update: Update):
        pass