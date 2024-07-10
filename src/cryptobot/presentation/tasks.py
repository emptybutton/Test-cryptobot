import asyncio

from cryptobot.facade import services


async def run_tasks() -> None:
    await _notification_task()


async def _notification_task() -> None:
    while True:
        await asyncio.sleep(30)
        await services.notify.perform()
