"""
Это не совсем репы как они есть в DDD, но они, как по мне, достаточно к ним
приближены, нежели чем к шлюзам в том виде в котором они есть в этом проекте.
"""

from abc import ABC, abstractmethod
from typing import Optional, AsyncIterable
from uuid import UUID

from cryptobot.domain.entities import User, Tracking, Cryptocurrency


class Users(ABC):
    @abstractmethod
    async def add(self, user: User) -> None: ...

    @abstractmethod
    async def find_by_telegram_chat_id(
        self,
        telegram_chat_id: int,
    ) -> Optional[User]: ...

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[User]: ...


class Trackings(ABC):
    @abstractmethod
    async def add(self, tracking: Tracking) -> None: ...

    @abstractmethod
    async def find_by_cryptocurrency_id(
        self,
        cryptocurrency_id: str,
    ) -> AsyncIterable[Tracking]: ...


class Cryptocurrencies(ABC, AsyncIterable[Tracking]):
    @abstractmethod
    async def add(self, cryptocurrency: Cryptocurrency) -> None: ...

    @abstractmethod
    async def update(self, cryptocurrency: Cryptocurrency) -> None: ...

    @abstractmethod
    async def find_by_symbol(
        self,
        symbol: str,
    ) -> Optional[Cryptocurrency]: ...
