"""
Тут много где нужно получить множество экземпляров (особенно в
`Cryptocurrencies.__aiter__`). На данный момент, без нагрузки, это ок, но в
случае её появление стоило бы пагинировать запросы, путем добавления
`__page_size` в подобные классы и отправкой множества запросов с `offset` и
`limit` по нему, благо тут используются генераторы и сами "страницы" будут
очищатся сборщиком мусора.
"""

from typing import Optional, AsyncIterable, AsyncIterator
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from cryptobot.application.ports import repos
from cryptobot.domain import entities, vos
from cryptobot.periphery.db import tables


class Users(repos.Users):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, user: entities.User) -> None:
        stmt = insert(tables.User).values(
            id=user.id,
            telegram_chat_id=user.telegram_chat_id,
        )

        await self.session.execute(stmt)

    async def find_by_telegram_chat_id(
        self,
        telegram_chat_id: int,
    ) -> Optional[entities.User]:
        query = (
            select(tables.User.id)
            .where(tables.User.telegram_chat_id == telegram_chat_id)
            .limit(1)
        )

        results = await self.session.execute(query)
        raw_user = results.first()

        if raw_user is None:
            return None

        return entities.User(
            id=raw_user.id,
            telegram_chat_id=telegram_chat_id,
        )

    async def find_by_id(self, id: UUID) -> Optional[entities.User]:
        query = (
            select(tables.User.telegram_chat_id)
            .where(tables.User.id == id)
            .limit(1)
        )

        results = await self.session.execute(query)
        raw_user = results.first()

        if raw_user is None:
            return None

        return entities.User(
            id=id,
            telegram_chat_id=raw_user.telegram_chat_id,
        )


class Trackings(repos.Trackings):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, tracking: entities.Tracking) -> None:
        stmt = insert(tables.Tracking).values(
            id=tracking.id,
            user_id=tracking.user_id,
            cryptocurrency_id=tracking.cryptocurrency_id,
            lower_threshold_dollars=tracking.lower_threshold.dollars.amount,
            upper_threshold_dollars=tracking.upper_threshold.dollars.amount,
        )

        await self.session.execute(stmt)

    async def find_by_cryptocurrency_id(
        self,
        cryptocurrency_id: str,
    ) -> AsyncIterable[entities.Tracking]:
        query = (
            select(
                tables.Tracking.id,
                tables.Tracking.user_id,
                tables.Tracking.lower_threshold_dollars,
                tables.Tracking.upper_threshold_dollars,
            )
            .where(tables.Tracking.cryptocurrency_id == cryptocurrency_id)
        )

        results = await self.session.execute(query)

        for result in results.all():
            yield self.__tracking_of(result, cryptocurrency_id)

    def __tracking_of(
        self,
        data: object,
        cryptocurrency_id: str,
    ) -> entities.Tracking:
        lower_threshold_dollars = vos.Dollars(amount=data.lower_threshold_dollars)
        upper_threshold_dollars = vos.Dollars(amount=data.upper_threshold_dollars)

        return entities.Tracking(
            id=data.id,
            user_id=data.user_id,
            cryptocurrency_id=cryptocurrency_id,
            lower_threshold=vos.Threshold(dollars=lower_threshold_dollars),
            upper_threshold=vos.Threshold(dollars=upper_threshold_dollars),
        )


class Cryptocurrencies(repos.Cryptocurrencies):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, cryptocurrency: entities.Cryptocurrency) -> None:
        stmt = insert(tables.Cryptocurrency).values(
            id=cryptocurrency.id,
            symbol=cryptocurrency.symbol,
            in_dollars=cryptocurrency.in_dollars.amount,
        )

        await self.session.execute(stmt)

    async def __aiter__(self) -> AsyncIterator:
        query = (
            select(
                tables.Cryptocurrency.id,
                tables.Cryptocurrency.symbol,
                tables.Cryptocurrency.in_dollars,
            )
        )

        results = await self.session.execute(query)

        for result in results.all():
            yield self.__cryptocurrency_of(result)

    async def update(self, cryptocurrency: entities.Cryptocurrency) -> None:
        stmt = (
            update(tables.Cryptocurrency)
            .where(tables.Cryptocurrency.id == cryptocurrency.id)
            .values(
                symbol=cryptocurrency.symbol,
                in_dollars=cryptocurrency.in_dollars.amount,
            )
        )

        await self.session.execute(stmt)

    async def find_by_symbol(
        self,
        symbol: str,
    ) -> Optional[entities.Cryptocurrency]:
        query = (
            select(
                tables.Cryptocurrency.id,
                tables.Cryptocurrency.in_dollars,
            )
            .where(tables.Cryptocurrency.symbol == symbol)
            .limit(1)
        )

        results = await self.session.execute(query)
        raw_cryptocurrency = results.first()

        if raw_cryptocurrency is None:
            return None

        return entities.Cryptocurrency(
            id=raw_cryptocurrency.id,
            in_dollars=vos.Dollars(amount=raw_cryptocurrency.in_dollars),
            symbol=symbol,
        )

    def __cryptocurrency_of(self, data: object) -> entities.Cryptocurrency:
        return entities.Cryptocurrency(
            id=data.id,
            symbol=data.symbol,
            in_dollars=vos.Dollars(amount=data.in_dollars),
        )
