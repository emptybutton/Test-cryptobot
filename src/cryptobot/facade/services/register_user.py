from dataclasses import dataclass
from uuid import UUID

from cryptobot.application.cases import register_user
from cryptobot.facade import adapters
from cryptobot.periphery.db.sessions import postgres_session_factory


@dataclass(kw_only=True, frozen=True)
class OutputDTO:
    user_id: UUID
    user_telegram_chat_id: int


async def perform(telegram_chat_id: int) -> OutputDTO:
    async with postgres_session_factory() as session:
        user = await register_user.perform(
            telegram_chat_id,
            transaction=adapters.transactions.DBTransaction(session),
            users=adapters.repos.Users(session),
        )

    return OutputDTO(
        user_id=user.id,
        user_telegram_chat_id=user.telegram_chat_id,
    )
