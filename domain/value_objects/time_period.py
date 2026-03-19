from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class TimePeriod:
    label: str
    start_date: date
    end_date: date
    granularity: str
