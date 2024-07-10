import logging

from cryptobot.application.ports import loggers
from cryptobot.domain import entities


class Logger(loggers.Logger):
    def __init__(self, logger: logging.Logger) -> None:
        self.__logger = logger

    def log_out_of_sync_with_coinmarketcap(
        self,
        cryptocurrency: entities.Cryptocurrency,
    ) -> None:
        self.__logger.error(
            f"cryptocurrency with id = {cryptocurrency.id} and"
            f" symbol = {cryptocurrency.symbol} is in the database,"
            " but not in coinmarketcap"
        )

    def log_tracking_without_user(self, tracking: entities.Tracking) -> None:
        self.__logger.critical(
            f"user with id = {tracking.user_id} of tracking with id ="
            f" {tracking.id} does not exist"
        )

