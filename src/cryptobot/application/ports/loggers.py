from abc import ABC, abstractmethod

from cryptobot.domain.entities import Cryptocurrency, Tracking


class Logger(ABC):
    @abstractmethod
    def log_out_of_sync_with_coinmarketcap(
        self,
        cryptocurrency: Cryptocurrency,
    ) -> None: ...

    @abstractmethod
    def log_tracking_without_user(self, tracking: Tracking) -> None: ...

