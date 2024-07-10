from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from cryptobot.periphery.envs import Env


_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=Env.telegram_bot_token, default=_properties)
