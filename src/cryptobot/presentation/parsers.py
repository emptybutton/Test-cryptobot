from typing import Optional


def as_number(text: str) -> Optional[int]:
    try:
        return int(text)
    except ValueError:
        return None
