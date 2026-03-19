from application.ports.input_ports import DetectEmergingSkillsUseCase
from domain.entities.job_offer import JobOffer
from domain.entities.trend import Trend
from domain.services.trend_analyzer import TrendAnalyzer
from application.use_cases.analyze_trends import AnalyzeTrendsService


class DetectEmergingSkillsService(DetectEmergingSkillsUseCase):
    def __init__(self, analyzer: TrendAnalyzer | None = None) -> None:
        self.analyzer = analyzer or TrendAnalyzer()
        self.trend_service = AnalyzeTrendsService(self.analyzer)

    def execute(self, job_offers: list[JobOffer], period: str, threshold: float) -> list[Trend]:
        trends = self.trend_service.execute(job_offers, period)
        emerging = self.analyzer.detect_accelerated_growth(trends, threshold)
        for item in emerging:
            item.emerging = True
        return emerging
