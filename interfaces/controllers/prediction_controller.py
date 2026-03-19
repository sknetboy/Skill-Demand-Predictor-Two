from application.use_cases.analyze_trends import AnalyzeTrendsService
from application.use_cases.detect_emerging_skills import DetectEmergingSkillsService
from application.use_cases.extract_skills import ExtractSkillsService
from application.use_cases.predict_demand import PredictDemandService
from infrastructure.ml.models import MovingAverageForecastModel, RandomForestForecastModel
from infrastructure.ml.visualization import PlotlyVisualizationAdapter
from infrastructure.nlp.skill_extractor import SkillExtractor
from infrastructure.repositories.job_data_repository import FileJobDataRepository
from infrastructure.repositories.skill_repository import InMemorySkillRepository


class PredictionController:
    def __init__(self) -> None:
        self.job_repository = FileJobDataRepository()
        self.skill_repository = InMemorySkillRepository()
        self.extract_service = ExtractSkillsService(SkillExtractor(), self.skill_repository)
        self.trend_service = AnalyzeTrendsService()
        self.emerging_service = DetectEmergingSkillsService()
        self.visualization = PlotlyVisualizationAdapter()

    def _load_enriched_offers(self, source: str):
        offers = self.job_repository.load_job_offers(source)
        return self.extract_service.execute(offers)

    def extract_skills(self, source: str) -> dict:
        offers = self._load_enriched_offers(source)
        return {
            "offers": [
                {
                    "offer_id": offer.offer_id,
                    "title": offer.title,
                    "skills": [skill.__dict__ for skill in offer.skills],
                }
                for offer in offers
            ]
        }

    def analyze_trends(self, source: str, period: str) -> dict:
        offers = self._load_enriched_offers(source)
        trends = self.trend_service.execute(offers, period)
        return self.visualization.build_skill_trends(trends)

    def predict_demand(self, source: str, period: str, horizon: int, model_name: str) -> dict:
        offers = self._load_enriched_offers(source)
        model = RandomForestForecastModel() if model_name == "random_forest" else MovingAverageForecastModel()
        forecasts = PredictDemandService(model).execute(offers, period, horizon)
        return self.visualization.build_skill_trends(forecasts)

    def detect_emerging_skills(self, source: str, period: str, threshold: float) -> dict:
        offers = self._load_enriched_offers(source)
        trends = self.emerging_service.execute(offers, period, threshold)
        return self.visualization.build_skill_trends(trends)

    def dashboard_summary(self, source: str, period: str = "monthly") -> dict:
        offers = self._load_enriched_offers(source)
        trends = self.trend_service.execute(offers, period)
        forecasts = PredictDemandService(MovingAverageForecastModel()).execute(offers, period, horizon=3)
        emerging = self.emerging_service.execute(offers, period, threshold=0.5)
        return {
            "trend_count": len(trends),
            "forecast_count": len(forecasts),
            "emerging_skills": [trend.skill_name for trend in emerging],
            "top_skills": sorted(
                [
                    {"skill": trend.skill_name, "frequency": trend.frequency}
                    for trend in trends
                ],
                key=lambda item: item["frequency"],
                reverse=True,
            )[:10],
        }
