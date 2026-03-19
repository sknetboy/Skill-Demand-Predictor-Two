from collections import defaultdict
from application.ports.input_ports import PredictDemandUseCase
from application.ports.output_ports import MLModelPort
from domain.entities.job_offer import JobOffer
from domain.entities.trend import Trend
from domain.services.trend_analyzer import TrendAnalyzer
from application.use_cases.analyze_trends import AnalyzeTrendsService


class PredictDemandService(PredictDemandUseCase):
    def __init__(self, model: MLModelPort, analyzer: TrendAnalyzer | None = None) -> None:
        self.model = model
        self.analyzer = analyzer or TrendAnalyzer()
        self.trend_service = AnalyzeTrendsService(self.analyzer)

    def execute(self, job_offers: list[JobOffer], period: str, horizon: int) -> list[Trend]:
        trends = self.trend_service.execute(job_offers, period)
        by_skill: dict[str, list[Trend]] = defaultdict(list)
        for trend in trends:
            by_skill[trend.skill_name].append(trend)

        forecasts: list[Trend] = []
        for skill_name, skill_trends in by_skill.items():
            ordered = sorted(skill_trends, key=lambda item: item.period)
            values = [trend.frequency for trend in ordered]
            predicted = self.model.train_and_forecast(values, horizon)
            base_period = ordered[-1].period
            for idx, value in enumerate(predicted, start=1):
                forecasts.append(
                    Trend(
                        skill_name=skill_name,
                        category=ordered[-1].category,
                        period=f"{base_period}+{idx}",
                        frequency=int(round(value)),
                        growth_rate=0.0,
                        forecast=float(value),
                    )
                )
        return forecasts
