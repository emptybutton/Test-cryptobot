from dataclasses import dataclass
from typing import Self


@dataclass(kw_only=True, frozen=True)
class Dollars:
    amount: int

    def __gt__(self, other: Self) -> bool:
        return self.amount > other.amount

    def __ge__(self, other: Self) -> bool:
        return self.amount >= other.amount


@dataclass(kw_only=True, frozen=True)
class Threshold:
    dollars: Dollars

    def __gt__(self, other: Self) -> bool:
        return self.dollars > other.dollars

    def __ge__(self, other: Self) -> bool:
        return self.dollars >= other.dollars
