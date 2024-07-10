from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from cryptobot.application.cases import add_tracking
from cryptobot.facade import adapters
from cryptobot.periphery.envs import Env
from cryptobot.periphery.db.sessions import postgres_session_factory


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    tracking_id: UUID
    user_id: UUID
    cryptocurrency_id: str
    upper_threshold: int
    lower_threshold: int


BaseError: TypeAlias = add_tracking.BaseError

NoCryptocurrencyError: TypeAlias = add_tracking.NoCryptocurrencyError

CoinmarketcapIsNotWorkingError: TypeAlias = (
    add_tracking.CoinmarketcapIsNotWorkingError
)


async def perform(
    telegram_chat_id: int,
    cryptocurrency_symbol: str,
    first_threshold_dollars: int,
    second_threshold_dollars: int,
) -> OutputDTO:
    async with postgres_session_factory() as session:
        tracking = await add_tracking.perform(
            telegram_chat_id,
            cryptocurrency_symbol,
            first_threshold_dollars,
            second_threshold_dollars,
            transaction=adapters.transactions.DBTransaction(session),
            users=adapters.repos.Users(session),
            trackings=adapters.repos.Trackings(session),
            cryptocurrencies=adapters.repos.Cryptocurrencies(session),
            coinmarketcap_gateway=adapters.gateways.CoinmarketcapGateway(),
            coinmarketcap_token=Env.coinmarketcap_token,
        )

    return OutputDTO(
        tracking_id=tracking.id,
        user_id=tracking.user_id,
        cryptocurrency_id=tracking.cryptocurrency_id,
        upper_threshold=tracking.upper_threshold.dollars.amount,
        lower_threshold=tracking.lower_threshold.dollars.amount,
    )
