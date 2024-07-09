import asyncio
import logging
import sys

from faststream import FastStream

from src.periphery.bots import bot
from src.periphery.brokers import redis_broker
from src.presentation.bot_dispatching import dispatcher
from src.presentation.event_routes import router


async def start_aiogram() -> None:
    await dispatcher.start_polling(bot)


async def start_faststream() -> None:
    app = FastStream(redis_broker)
    redis_broker.include_router(router)

    await app.run()


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await asyncio.gather(start_faststream(), start_aiogram())


if __name__ == "__main__":
    asyncio.run(main())
