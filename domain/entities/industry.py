from dataclasses import dataclass


@dataclass(frozen=True)
class Industry:
    name: str
    sector_code: str | None = None
