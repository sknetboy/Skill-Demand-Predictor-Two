from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class CurriculumProgram:
    name: str
    skills_covered: Set[str]
    description: str = ""

@dataclass
class CurriculumGap:
    skill_name: str
    market_demand: int
    curriculum_coverage: float  # 0 to 1
    priority: str  # Critical, High, Medium
    recommendation: str
