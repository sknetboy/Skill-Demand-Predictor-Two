from dataclasses import dataclass
from domain.value_objects.skill_category import SkillCategory


@dataclass
class Trend:
    skill_name: str
    category: SkillCategory
    period: str
    frequency: int
    growth_rate: float
    forecast: float | None = None
    emerging: bool = False
