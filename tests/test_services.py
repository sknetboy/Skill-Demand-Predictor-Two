from application.use_cases.analyze_trends import AnalyzeTrendsService
from application.use_cases.detect_emerging_skills import DetectEmergingSkillsService
from application.use_cases.extract_skills import ExtractSkillsService
from application.use_cases.predict_demand import PredictDemandService
from infrastructure.ml.models import MovingAverageForecastModel
from infrastructure.nlp.skill_extractor import SkillExtractor
from infrastructure.repositories.job_data_repository import FileJobDataRepository
from infrastructure.repositories.skill_repository import InMemorySkillRepository


SOURCE = "data/raw/job_offers_sample.csv"


def build_offers():
    repository = FileJobDataRepository()
    offers = repository.load_job_offers(SOURCE)
    return ExtractSkillsService(SkillExtractor(), InMemorySkillRepository()).execute(offers)


def test_skill_extraction_loads_skills():
    offers = build_offers()
    assert any(skill.name == "python" for skill in offers[0].skills)


def test_trend_analysis_returns_records():
    offers = build_offers()
    trends = AnalyzeTrendsService().execute(offers, "monthly")
    assert trends
    assert all(trend.period.startswith("2025-") for trend in trends)


def test_prediction_returns_horizon_per_skill():
    offers = build_offers()
    forecast = PredictDemandService(MovingAverageForecastModel()).execute(offers, "monthly", 2)
    assert forecast
    assert any(item.period.endswith("+1") for item in forecast)


def test_emerging_skills_marks_records():
    offers = build_offers()
    emerging = DetectEmergingSkillsService().execute(offers, "monthly", 0)
    assert all(item.emerging for item in emerging)
