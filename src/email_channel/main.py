#!/usr/bin/env python3

from loguru import logger

from kafka_consumer.consumer import EmailKafkaConsumer


logger.info("Main script start")


def main():
    kafka_consumer = EmailKafkaConsumer()
    kafka_consumer.start()
    logger.info("after start in main")


main()
