"""
Приходится каждый раз сканировать всю базу данных, что пока ок, но при большом
ее объеме будет очень долго, может даже больше чем 30 секунд.

В случае когда вертикальное масштабирование уже может не помогать, можно
каким-нибудь способом шардировать БД и установить для каждого такого шарда
отдельного воркера. Пока даже несколько воркеров нельзя запускать.
"""

import asyncio

from cryptobot.facade import services


async def run_tasks() -> None:
    await _notification_task()


async def _notification_task() -> None:
    while True:
        await asyncio.sleep(30)
        await services.notify.perform()
