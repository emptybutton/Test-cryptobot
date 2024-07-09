from cryptobot.application import ports


class BaseError(Exception): ...


class NoUserError(BaseError): ...


async def perform(
    *,
    users: ports.repos.Users,
    trackings: ports.repos.Trackings,
    cryptocurrencies: ports.repos.Cryptocurrencies,
    coinmarketcap_gateway: ports.gateways.CoinmarketcapGateway,
    coinmarketcap_token: str,
    telegram_notification_gateway: ports.gateways.TelegramNotificationGateway,
    logger: ports.loggers.Logger,
) -> None:
    async for local_cryptocurrency in cryptocurrencies:
        cryptocurrency_trackings = await trackings.find_by_cryptocurrency_id(
            local_cryptocurrency.id
        )

        result = await coinmarketcap_gateway.find_by_symbol(
            local_cryptocurrency.symbol,
            token=coinmarketcap_token,
        )

        if result is ports.gateways.CoinmarketcapGatewayBadResult.denied:
            continue

        if result is ports.gateways.CoinmarketcapGatewayBadResult.no_cryptocurrency:
            logger.log_out_of_sync_with_coinmarketcap(local_cryptocurrency)
            continue

        exchange_cryptocurrency = result

        async for tracking in cryptocurrency_trackings:
            user = await users.find_by_id(tracking.user_id)

            if user is None:
                logger.log_tracking_without_user(tracking)
                continue

            if tracking.was_there_passage_up(exchange_cryptocurrency, local_cryptocurrency):
                await telegram_notification_gateway.notify_about_passage_up(
                    user, tracking, exchange_cryptocurrency
                )

            elif tracking.was_there_passage_down(exchange_cryptocurrency, local_cryptocurrency):
                await telegram_notification_gateway.notify_about_passage_down(
                    user, tracking, exchange_cryptocurrency
                )

            elif tracking.was_there_top_entry(exchange_cryptocurrency, local_cryptocurrency):
                await telegram_notification_gateway.notify_top_entry(
                    user, tracking, exchange_cryptocurrency
                )

            elif tracking.was_there_bottom_entry(exchange_cryptocurrency, local_cryptocurrency):
                await telegram_notification_gateway.notify_bottom_entry(
                    user, tracking, exchange_cryptocurrency
                )

            elif tracking.was_there_top_exit(exchange_cryptocurrency, local_cryptocurrency):
                await telegram_notification_gateway.notify_about_top_exit(
                    user, tracking, exchange_cryptocurrency
                )

            elif tracking.was_there_bottom_exit(exchange_cryptocurrency, local_cryptocurrency):
                await telegram_notification_gateway.notify_about_bottom_exit(
                    user, tracking, exchange_cryptocurrency
                )

            await cryptocurrencies.update(exchange_cryptocurrency)
