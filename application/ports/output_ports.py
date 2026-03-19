from abc import ABC, abstractmethod
from domain.entities.job_offer import JobOffer
from domain.entities.skill import Skill
from domain.entities.trend import Trend


class JobDataRepositoryPort(ABC):
    @abstractmethod
    def load_job_offers(self, source: str) -> list[JobOffer]: ...


class SkillRepositoryPort(ABC):
    @abstractmethod
    def save_skills(self, skills: list[Skill]) -> None: ...


class MLModelPort(ABC):
    @abstractmethod
    def train_and_forecast(self, series: list[float], horizon: int) -> list[float]: ...


class VisualizationPort(ABC):
    @abstractmethod
    def build_skill_trends(self, trends: list[Trend]) -> dict: ...
