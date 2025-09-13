#!/usr/bin/env python3
from loguru import logger
from kafka_consumer.consumer import TelegramKafkaConsumer
from telegram.telegram_bot import TelegramBot

logger.info("Main script start")


def main():
    tg_bot = TelegramBot()
    kafka_consumer = TelegramKafkaConsumer(tg_bot=tg_bot)
    kafka_consumer.start()
    logger.info("after start in main")


main()
