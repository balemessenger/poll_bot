# In the name of God

import inspect

from loguru import logger


class Sender:
    def __init__(self, bot):
        self.bot = bot

    def send_message(self, chat_id, text, reply_markup=None):
        self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        logger.info(inspect.stack()[1][3])

    def send_photo(self, chat_id, photo_path, caption, reply_markup=None):
        self.bot.send_photo(chat_id=chat_id, caption=caption, photo=open(photo_path, "rb"), reply_markup=reply_markup)
        logger.info(inspect.stack()[1][3])
