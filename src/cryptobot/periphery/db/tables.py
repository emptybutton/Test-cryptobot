from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"db.{type(self).__name__}(id={self.id!r})"


class User(Base):
    __tablename__ = "users"

    telegram_chat_id: Mapped[int]


class Cryptocurrency(Base):
    __tablename__ = "cryptocurrencies"

    symbol: Mapped[str]
    in_dollars: Mapped[int]


class Tracking(Base):
    __tablename__ = "trackings"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    cryptocurrency_id: Mapped[int]
    lower_threshold_dollars: Mapped[int]
    upper_threshold_dollars: Mapped[int]
