from functools import partial

from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from cryptobot.presentation.parsers import as_number
from cryptobot.facade import services


dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.text != "/start":
        return

    await services.register_user.perform(message.chat.id)
    await message.answer("Привет! Введи /help для списка всех комманд")


@dispatcher.message(F.text == "/help")
async def command_help_handler(message: Message) -> None:
    text = (
        "Комманды:\n"
        "/start - перезапустить бота\n"
        "/track <название приптовалюты> <первое число диапазона>"
        " <второе число диапазона> - отслеживать криптовалюту"
    )
    await message.answer(text, parse_mode="Markdown")


@dispatcher.message(F.text[:6] == "/track")
async def command_track_handler(message: Message) -> None:
    answer = partial(message.answer, parse_mode="Markdown")
    words = message.text.split()
    arguments = words[1:]

    if len(arguments) != 3:
        await answer(
            "Неправильные аргументы. Пример правильных:\n"
            "/track BTC 5000 6000"
        )
        return

    cryptocurrency_symbol = arguments[0]
    first_threshold_dollars = as_number(arguments[1])
    second_threshold_dollars = as_number(arguments[2])

    if None in (first_threshold_dollars, second_threshold_dollars):
        await answer(
            "Неправильный диапазон. Пример правильного:\n"
            "/track BTC 5000 6000"
        )
        return

    try:
        await services.add_tracking.perform(
            message.chat.id,
            cryptocurrency_symbol,
            first_threshold_dollars,
            second_threshold_dollars,
        )
        await answer(f"Отслеживание \"{cryptocurrency_symbol}\" началось")
    except services.add_tracking.CoinmarketcapIsNotWorkingError:
        await answer("Произошла ошибка. Попробуйте позже")
    except services.add_tracking.NoCryptocurrencyError:
        await answer(f"Криптовалюты \"{cryptocurrency_symbol}\" не знаем")
