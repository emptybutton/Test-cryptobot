from cryptobot.domain import entities
from cryptobot.application import ports


async def perform(
    telegram_chat_id: int,
    *,
    transaction: ports.transactions.Transaction,
    users: ports.repos.Users,
) -> entities.User:
    async with transaction:
        user = await users.find_by_telegram_chat_id(telegram_chat_id)

        if user is not None:
            return user

        user = entities.User(telegram_chat_id=telegram_chat_id)
        await users.add(user)

        return user
