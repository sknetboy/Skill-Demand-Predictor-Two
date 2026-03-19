from abc import ABC, abstractmethod
from domain.entities.job_offer import JobOffer
from domain.entities.skill import Skill
from domain.entities.trend import Trend


class ExtractSkillsUseCase(ABC):
    @abstractmethod
    def execute(self, job_offers: list[JobOffer]) -> list[JobOffer]: ...


class AnalyzeTrendsUseCase(ABC):
    @abstractmethod
    def execute(self, job_offers: list[JobOffer], period: str) -> list[Trend]: ...


class PredictDemandUseCase(ABC):
    @abstractmethod
    def execute(self, job_offers: list[JobOffer], period: str, horizon: int) -> list[Trend]: ...


class DetectEmergingSkillsUseCase(ABC):
    @abstractmethod
    def execute(self, job_offers: list[JobOffer], period: str, threshold: float) -> list[Trend]: ...
