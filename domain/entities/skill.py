from dataclasses import dataclass, field
from domain.value_objects.skill_category import SkillCategory


@dataclass
class Skill:
    name: str
    category: SkillCategory = SkillCategory.UNKNOWN
    confidence: float = 1.0
    occurrences: int = 0
    metadata: dict[str, str] = field(default_factory=dict)
