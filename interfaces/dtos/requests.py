from pydantic import BaseModel, Field


class SourceRequest(BaseModel):
    source: str = Field(..., description="Ruta del archivo CSV o JSON con vacantes")
    period: str = Field(default="monthly", pattern="^(monthly|quarterly)$")


class PredictRequest(SourceRequest):
    horizon: int = Field(default=3, ge=1, le=12)
    model: str = Field(default="moving_average", pattern="^(moving_average|random_forest)$")


class EmergingSkillsRequest(SourceRequest):
    threshold: float = Field(default=0.5, ge=0)
