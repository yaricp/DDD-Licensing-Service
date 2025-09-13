import telebot
from loguru import logger

from settings import main_config

logger.info(f"TELEGRAM_BOT_TOKEN: {main_config.TELEGRAM_BOT_TOKEN}")
logger.info(f"ADMIN_CHAT_ID: {main_config.ADMIN_CHAT_ID}")


class TelegramBot:

    def __init__(self):
        self.telegram_bot_token = main_config.TELEGRAM_BOT_TOKEN
        self.admin_chat_id = main_config.ADMIN_CHAT_ID
        self.__bot = telebot.TeleBot(self.telegram_bot_token)

    def send_message(self, message: str):
        try:
            self.__bot.send_message(self.admin_chat_id, message)
        except Exception as e:
            logger.error(
                f'Error {e} while sending notification {message}'
            )
        return True
