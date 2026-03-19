from collections import defaultdict
from application.ports.input_ports import AnalyzeTrendsUseCase
from domain.entities.job_offer import JobOffer
from domain.entities.trend import Trend
from domain.services.trend_analyzer import TrendAnalyzer


class AnalyzeTrendsService(AnalyzeTrendsUseCase):
    def __init__(self, analyzer: TrendAnalyzer | None = None) -> None:
        self.analyzer = analyzer or TrendAnalyzer()

    def execute(self, job_offers: list[JobOffer], period: str) -> list[Trend]:
        labels = [self._period_label(offer, period) for offer in job_offers]
        return self.analyzer.calculate_trends(job_offers, labels)

    @staticmethod
    def _period_label(offer: JobOffer, period: str) -> str:
        if period == "quarterly":
            quarter = ((offer.published_at.month - 1) // 3) + 1
            return f"{offer.published_at.year}-Q{quarter}"
        return f"{offer.published_at.year}-{offer.published_at.month:02d}"
