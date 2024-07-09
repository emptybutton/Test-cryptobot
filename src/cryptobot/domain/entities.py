from dataclasses import dataclass, field
from uuid import UUID, uuid4

from cryptobot.domain.errors import (
    IncorrectOrderOfTrackingThresholdsError,
    TrackingInvoluntaryCryptocurrency,
)
from cryptobot.domain.vos import Threshold, Dollars


@dataclass(kw_only=True)
class User:
    id: UUID = field(default_factory=uuid4)
    telegram_chat_id: int


@dataclass(kw_only=True)
class Cryptocurrency:
    id: str
    symbol: str
    in_dollars: Dollars


@dataclass(kw_only=True)
class Tracking:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    cryptocurrency_id: str
    upper_threshold: Threshold
    lower_threshold: Threshold

    def __post_init__(self) -> None:
        if self.lower_threshold > self.upper_threshold:
            raise IncorrectOrderOfTrackingThresholdsError

    def __contains__(self, cryptocurrency: object) -> bool:
        return (
            isinstance(cryptocurrency, Cryptocurrency)
            and cryptocurrency.id == self.cryptocurrency_id
            and cryptocurrency.in_dollars >= self.lower_threshold.dollars
            and cryptocurrency.in_dollars <= self.upper_threshold.dollars
        )

    def __gt__(self, cryptocurrency: object) -> bool:
        return (
            isinstance(cryptocurrency, Cryptocurrency)
            and cryptocurrency.id == self.cryptocurrency_id
            and self.lower_threshold.dollars > cryptocurrency.in_dollars
        )

    def __lt__(self, cryptocurrency: object) -> bool:
        return (
            isinstance(cryptocurrency, Cryptocurrency)
            and cryptocurrency.id == self.cryptocurrency_id
            and self.upper_threshold.dollars < cryptocurrency.in_dollars
        )

    def was_there_passage_down(
        self,
        current_cryptocurrency: Cryptocurrency,
        old_cryptocurrency: Cryptocurrency,
    ) -> bool:
        self.__check_trackable(current_cryptocurrency, old_cryptocurrency)
        return current_cryptocurrency < self < old_cryptocurrency

    def was_there_passage_up(
        self,
        current_cryptocurrency: Cryptocurrency,
        old_cryptocurrency: Cryptocurrency,
    ) -> bool:
        self.__check_trackable(current_cryptocurrency, old_cryptocurrency)
        return old_cryptocurrency < self < current_cryptocurrency

    def was_there_top_entry(
        self,
        current_cryptocurrency: Cryptocurrency,
        old_cryptocurrency: Cryptocurrency,
    ) -> bool:
        self.__check_trackable(current_cryptocurrency, old_cryptocurrency)
        return current_cryptocurrency in self and self < old_cryptocurrency

    def was_there_bottom_entry(
        self,
        current_cryptocurrency: Cryptocurrency,
        old_cryptocurrency: Cryptocurrency,
    ) -> bool:
        self.__check_trackable(current_cryptocurrency, old_cryptocurrency)
        return current_cryptocurrency in self and old_cryptocurrency < self

    def was_there_bottom_exit(
        self,
        current_cryptocurrency: Cryptocurrency,
        old_cryptocurrency: Cryptocurrency,
    ) -> bool:
        self.__check_trackable(current_cryptocurrency, old_cryptocurrency)
        return old_cryptocurrency in self and current_cryptocurrency < self

    def was_there_top_exit(
        self,
        current_cryptocurrency: Cryptocurrency,
        old_cryptocurrency: Cryptocurrency,
    ) -> bool:
        self.__check_trackable(current_cryptocurrency, old_cryptocurrency)
        return old_cryptocurrency in self and self < current_cryptocurrency

    def __check_trackable(
        self,
        current_cryptocurrency: Cryptocurrency,
        old_cryptocurrency: Cryptocurrency,
    ) -> None:
        if not (
            self.cryptocurrency_id
            == current_cryptocurrency.id
            == old_cryptocurrency.id
        ):
            raise TrackingInvoluntaryCryptocurrency
