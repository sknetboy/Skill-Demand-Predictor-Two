from dataclasses import dataclass, field
from enum import Enum
from typing import List

class RecommendationAction(Enum):
    OPEN_NEW_COURSE = "Abrir nuevo curso"
    UPDATE_CONTENT = "Actualizar contenidos"
    LAUNCH_CERTIFICATION = "Lanzar certificación"
    OBSOLETE_WARNING = "Posible obsolescencia"
    MONITOR = "Monitorear"

@dataclass
class AcademicRecommendation:
    skill_name: str
    action: RecommendationAction
    reason: str
    priority: str  # High, Medium, Low
    confidence_score: float
    current_frequency: int
    forecasted_growth: float
