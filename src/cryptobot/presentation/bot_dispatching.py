from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from cryptobot.presentation.parsers import as_number
from cryptobot.facade import services


dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await services.register_user.perform(message.chat.id)
    await message.answer("Привет! Введи /help для списка всех комманд")


@dispatcher.message()
async def command_help_handler(message: Message) -> None:
    if message.text != "/help":
        return

    await message.answer(
        "Комманды:\n"
        "/start - перезапусе бота\n"
        "/track <название приптовалюты> <первое число диапазона>"
        " <второе число диапазона> - отслеживать криптовалюту"
    )


@dispatcher.message()
async def command_track_handler(message: Message) -> None:
    if message.text != "/track":
        return

    words = message.text.split()
    arguments = words[1:]

    if len(arguments) != 3:
        await message.answer(
            "Неправильные аргументы. Пример правильных:\n"
            "/track BTC 5000 6000"
        )
        return

    cryptocurrency_symbol = arguments[0]
    first_threshold_dollars = as_number(arguments[1])
    second_threshold_dollars = as_number(arguments[2])

    if None in (first_threshold_dollars, second_threshold_dollars):
        await message.answer(
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
        await message.answer("Отслеживание \"{cryptocurrency_symbol}\" началось")
    except services.add_tracking.CoinmarketcapIsNotWorkingError:
        await message.answer("Произошла ошибка. Попробуйте позже")
    except services.add_tracking.NoCryptocurrencyError:
        await message.answer(f"Криптовалюты \"{cryptocurrency_symbol}\" не знаем")
