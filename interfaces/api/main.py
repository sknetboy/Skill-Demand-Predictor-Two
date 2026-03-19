from fastapi import FastAPI
from config.settings import get_settings
from interfaces.controllers.prediction_controller import PredictionController
from interfaces.dtos.requests import EmergingSkillsRequest, PredictRequest, SourceRequest

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
controller = PredictionController()


@app.get("/health")
def healthcheck() -> dict:
    return {"status": "ok", "service": settings.app_name}


@app.post("/api/v1/skills/extract")
def extract_skills(payload: SourceRequest) -> dict:
    return controller.extract_skills(payload.source)


@app.post("/api/v1/trends/analyze")
def analyze_trends(payload: SourceRequest) -> dict:
    return controller.analyze_trends(payload.source, payload.period)


@app.post("/api/v1/demand/predict")
def predict_demand(payload: PredictRequest) -> dict:
    return controller.predict_demand(payload.source, payload.period, payload.horizon, payload.model)


@app.post("/api/v1/skills/emerging")
def detect_emerging(payload: EmergingSkillsRequest) -> dict:
    return controller.detect_emerging_skills(payload.source, payload.period, payload.threshold)


@app.get("/api/v1/dashboard/summary")
def dashboard_summary(source: str = "data/raw/job_offers_sample.csv", period: str = "monthly") -> dict:
    return controller.dashboard_summary(source, period)
