from sqlalchemy.ext.asyncio import AsyncSession

from cryptobot.application.ports import repos
from cryptobot.domain.entities import User

class Users(repos.Users):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, user: User) -> None:
        

    async def find_by_telegram_chat_id(
        self,
        telegram_chat_id: int,
    ) -> Optional[User]: ...

    async def find_by_id(self, id: UUID) -> Optional[User]: ...


class Trackings(ABC):
    async def add(self, tracking: Tracking) -> None: ...

    async def find_by_cryptocurrency_id(
        self,
        cryptocurrency_id: str,
    ) -> AsyncIterable[Tracking]: ...


class Cryptocurrencies(ABC, AsyncIterable[Tracking]):
    async def add(self, cryptocurrency: Cryptocurrency) -> None: ...

    async def update(self, cryptocurrency: Cryptocurrency) -> None: ...

    async def find_by_symbol(
        self,
        symbol: str,
    ) -> Optional[Cryptocurrency]: ...
