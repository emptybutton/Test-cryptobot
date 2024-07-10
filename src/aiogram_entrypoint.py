import asyncio
import logging
import sys

from cryptobot.periphery.bots import bot
from cryptobot.presentation.bot_dispatching import dispatcher


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
