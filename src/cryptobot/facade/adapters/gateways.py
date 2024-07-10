import aiogram
import aiohttp

from cryptobot.application.ports import gateways
from cryptobot.domain import entities, vos


class TelegramNotificationGateway(gateways.TelegramNotificationGateway):
    def __init__(self, bot: aiogram.Bot) -> None:
        self.__bot = bot

    async def notify_top_entry(
        self,
        user: entities.User,
        tracking: entities.Tracking,
        cryptocurrency: entities.Cryptocurrency,
    ) -> None:
        message = (
            f"{cryptocurrency.symbol} опустился ниже верхней границы в"
            " {tracking.upper_threshold.dollars.amount}$"
        )
        await self.__bot.send_message(user.telegram_chat_id, message)

    async def notify_bottom_entry(
        self,
        user: entities.User,
        tracking: entities.Tracking,
        cryptocurrency: entities.Cryptocurrency,
    ) -> None:
        message = (
            f"{cryptocurrency.symbol} привысил нижнюю границу в"
            " {tracking.lower_threshold.dollars.amount}$"
        )
        await self.__bot.send_message(user.telegram_chat_id, message)

    async def notify_about_top_exit(
        self,
        user: entities.User,
        tracking: entities.Tracking,
        cryptocurrency: entities.Cryptocurrency,
    ) -> None:
        message = (
            f"{cryptocurrency.symbol} привысил верхнюю границу в"
            " {tracking.upper_threshold.dollars.amount}$"
        )
        await self.__bot.send_message(user.telegram_chat_id, message)

    async def notify_about_bottom_exit(
        self,
        user: entities.User,
        tracking: entities.Tracking,
        cryptocurrency: entities.Cryptocurrency,
    ) -> None:
        message = (
            f"{cryptocurrency.symbol} опустился ниже нижней границы в"
            " {tracking.lower_threshold.dollars.amount}$"
        )
        await self.__bot.send_message(user.telegram_chat_id, message)

    async def notify_about_passage_down(
        self,
        user: entities.User,
        tracking: entities.Tracking,
        cryptocurrency: entities.Cryptocurrency,
    ) -> None:
        message = (
            f"{cryptocurrency.symbol} упал ниже как верхней так и нижней границы"
            f" в {tracking.upper_threshold.dollars.amount}$ и"
            f" {tracking.lower_threshold.dollars.amount}$"
        )
        await self.__bot.send_message(user.telegram_chat_id, message)

    async def notify_about_passage_up(
        self,
        user: entities.User,
        tracking: entities.Tracking,
        cryptocurrency: entities.Cryptocurrency,
    ) -> None:
        message = (
            f"{cryptocurrency.symbol} привысил как верхнюю так и нижнюю границы"
            f" в {tracking.upper_threshold.dollars.amount}$ и"
            f" {tracking.lower_threshold.dollars.amount}$"
        )
        await self.__bot.send_message(user.telegram_chat_id, message)


class CoinmarketcapGateway(gateways.CoinmarketcapGateway):
    async def find_by_symbol(
        self,
        symbol: str,
        *,
        token: str,
    ) -> entities.Cryptocurrency | gateways.CoinmarketcapGatewayBadResult:
        url = "https://pro-api.coinmarketcap.com/v2/tools/price-conversion"
        params = {"amount": 1, "symbol": symbol}
        headers = {"X-CMC_PRO_API_KEY": token}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers, ssl=False) as response:
                if response.status != 200:
                    return gateways.CoinmarketcapGatewayBadResult.denied

                response_body = await response.json()

        raw_cryptocurrencies = response_body["data"]

        if len(raw_cryptocurrencies) == 0:
            return gateways.CoinmarketcapGatewayBadResult.no_cryptocurrency

        raw_cryptocurrency = raw_cryptocurrencies[0]

        id = str(raw_cryptocurrency["id"])
        price = int(raw_cryptocurrency["quote"]["USD"]["price"])

        return entities.Cryptocurrency(
            id=id,
            symbol=symbol,
            in_dollars=vos.Dollars(amount=price),
        )
