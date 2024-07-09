from abc import ABC, abstractmethod
from enum import Enum, auto

from cryptobot.domain.entities import User, Tracking, Cryptocurrency


class CoinmarketcapGatewayBadResult(Enum):
    denied = auto()
    no_cryptocurrency = auto()


class CoinmarketcapGateway(ABC):
    @abstractmethod
    async def find_by_symbol(
        self,
        symbol: str,
        *,
        token: str,
    ) -> Cryptocurrency | CoinmarketcapGatewayBadResult: ...


class TelegramNotificationGateway(ABC):
    @abstractmethod
    async def notify_top_entry(
        self,
        user: User,
        tracking: Tracking,
        cryptocurrency: Cryptocurrency,
    ) -> None: ...

    @abstractmethod
    async def notify_bottom_entry(
        self,
        user: User,
        tracking: Tracking,
        cryptocurrency: Cryptocurrency,
    ) -> None: ...

    @abstractmethod
    async def notify_about_top_exit(
        self,
        user: User,
        tracking: Tracking,
        cryptocurrency: Cryptocurrency,
    ) -> None: ...

    @abstractmethod
    async def notify_about_bottom_exit(
        self,
        user: User,
        tracking: Tracking,
        cryptocurrency: Cryptocurrency,
    ) -> None: ...

    @abstractmethod
    async def notify_about_passage_down(
        self,
        user: User,
        tracking: Tracking,
        cryptocurrency: Cryptocurrency,
    ) -> None: ...

    @abstractmethod
    async def notify_about_passage_up(
        self,
        user: User,
        tracking: Tracking,
        cryptocurrency: Cryptocurrency,
    ) -> None: ...
