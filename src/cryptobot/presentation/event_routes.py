from faststream.redis import RedisRouter

from src.cases import users
from src.periphery.bots import bot


router = RedisRouter()


@router.subscriber("multiplication_occurred")
async def handle_response(
    a: int,
    b: int,
    result: int,
) -> None:
    message = f"Кто то умножил {a} на {b} и получил {result}"
    chat_ids = await users.get_all_chat_ids()

    for chat_id in chat_ids:
        await bot.send_message(chat_id, message)
