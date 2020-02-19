# In the name of God
import logging
from loguru import logger
from telegram import Bot
from telegram.ext import Updater

from polling_bot.config import Config
from polling_bot.db.base import Base, engine
from polling_bot.state_machine.state_machine import StateMachine

if __name__ == '__main__':
    logger.info("bot started")
    logging.basicConfig(level=logging.INFO)
    Base.metadata.create_all(engine)
    bot = Bot(token=Config.token, base_url=Config.base_url, base_file_url=Config.base_file_url)
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher
    StateMachine(dispatcher).start()
    updater.start_polling(poll_interval=0.25)
