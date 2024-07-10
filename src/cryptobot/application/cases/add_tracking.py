from cryptobot.domain import entities, vos
from cryptobot.application import ports


class BaseError(Exception): ...


class NoCryptocurrencyError(BaseError): ...


class CoinmarketcapIsNotWorkingError(BaseError): ...


async def perform(
    telegram_chat_id: int,
    cryptocurrency_symbol: str,
    first_threshold_dollars: int,
    second_threshold_dollars: int,
    *,
    transaction: ports.transactions.Transaction,
    users: ports.repos.Users,
    trackings: ports.repos.Trackings,
    cryptocurrencies: ports.repos.Cryptocurrencies,
    coinmarketcap_gateway: ports.gateways.CoinmarketcapGateway,
    coinmarketcap_token: str,
) -> entities.Tracking:
    async with transaction:
        user = await users.find_by_telegram_chat_id(telegram_chat_id)

        if user is None:
            user = entities.User(telegram_chat_id=telegram_chat_id)
            await users.add(user)

    lower_threshold = vos.Threshold(
        dollars=vos.Dollars(amount=first_threshold_dollars)
    )
    upper_threshold = vos.Threshold(
        dollars=vos.Dollars(amount=second_threshold_dollars)
    )

    if lower_threshold > upper_threshold:
        upper_threshold, lower_threshold = lower_threshold, upper_threshold

    async with transaction:
        cryptocurrency = await cryptocurrencies.find_by_symbol(cryptocurrency_symbol)

        if cryptocurrency is None:
            result = await coinmarketcap_gateway.find_by_symbol(
                cryptocurrency_symbol,
                token=coinmarketcap_token,
            )

            if result is ports.gateways.CoinmarketcapGatewayBadResult.no_cryptocurrency:
                raise NoCryptocurrencyError

            if result is ports.gateways.CoinmarketcapGatewayBadResult.denied:
                raise CoinmarketcapIsNotWorkingError

            cryptocurrency = result
            await cryptocurrencies.add(cryptocurrency)

        tracking = entities.Tracking(
            user_id=user.id,
            cryptocurrency_id=cryptocurrency.id,
            lower_threshold=lower_threshold,
            upper_threshold=upper_threshold,
        )
        await trackings.add(tracking)

        return tracking
