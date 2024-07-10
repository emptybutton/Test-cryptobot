import asyncio

from cryptobot.presentation.tasks import run_tasks


async def main() -> None:
    await run_tasks()


if __name__ == "__main__":
    asyncio.run(main())
