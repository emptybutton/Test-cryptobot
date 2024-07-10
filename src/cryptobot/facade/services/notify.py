from cryptobot.application.cases import notify
from cryptobot.facade import adapters
from cryptobot.periphery.envs import Env
from cryptobot.periphery.db.sessions import postgres_session_factory
from cryptobot.periphery import loggers, bots


async def perform() -> None:
    notification_gateway = adapters.gateways.TelegramNotificationGateway(bots.bot)

    async with postgres_session_factory() as session:
        await notify.perform(
            transaction=adapters.transactions.DBTransaction(session),
            users=adapters.repos.Users(session),
            trackings=adapters.repos.Trackings(session),
            cryptocurrencies=adapters.repos.Cryptocurrencies(session),
            coinmarketcap_gateway=adapters.gateways.CoinmarketcapGateway(),
            coinmarketcap_token=Env.coinmarketcap_token,
            telegram_notification_gateway=notification_gateway,
            logger=adapters.loggers.Logger(loggers.main_logger),
        )
