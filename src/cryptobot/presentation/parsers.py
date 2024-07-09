from typing import Optional


def number_pair_from(text: str) -> Optional[tuple[int, int]]:
    values = text.split(' ')

    if len(values) != 2:
        return None

    number_pair = tuple(map(_numeric, values))

    if all(number is not None for number in number_pair):
        return number_pair


def _numeric(text: str) -> Optional[int]:
    try:
        return int(text)
    except ValueError:
        return None
