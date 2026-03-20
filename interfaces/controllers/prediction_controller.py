from application.use_cases.analyze_trends import AnalyzeTrendsService
from application.use_cases.detect_emerging_skills import DetectEmergingSkillsService
from application.use_cases.extract_skills import ExtractSkillsService
from application.use_cases.predict_demand import PredictDemandService
from infrastructure.ml.models import MovingAverageForecastModel, RandomForestForecastModel
from infrastructure.ml.visualization import PlotlyVisualizationAdapter
from infrastructure.nlp.skill_extractor import SkillExtractor
from infrastructure.repositories.job_data_repository import FileJobDataRepository
from infrastructure.repositories.skill_repository import InMemorySkillRepository
from domain.services.academic_planner import AcademicPlannerService
from domain.services.gap_analyzer import GapAnalyzerService
from domain.entities.curriculum import CurriculumProgram
from domain.services.report_service import AcademicReportService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.repositories.sql_program_repository import SQLProgramRepository
from infrastructure.database.models import Base
from config.settings import get_settings


class PredictionController:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.job_repository = FileJobDataRepository()
        self.skill_repository = InMemorySkillRepository()
        self.extract_service = ExtractSkillsService(SkillExtractor(), self.skill_repository)
        self.trend_service = AnalyzeTrendsService()
        self.emerging_service = DetectEmergingSkillsService()
        self.visualization = PlotlyVisualizationAdapter()
        self.academic_planner = AcademicPlannerService()
        self.gap_analyzer = GapAnalyzerService()
        
        # Setup DB Session
        try:
            self.engine = create_engine(self.settings.database_url)
            # Create tables if they don't exist
            Base.metadata.create_all(bind=self.engine)
            
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.program_repository = SQLProgramRepository(self.SessionLocal())
            self.program_repository.seed_initial_data()
        except Exception as e:
            print(f"Warning: Could not connect to DB or create tables, using mock data. Error: {e}")
            self.program_repository = None
            self.mock_curriculum = [
                CurriculumProgram(name="Bootcamp Data Science", skills_covered={"python", "sql", "pandas", "numpy", "scikit-learn"}),
                CurriculumProgram(name="Especialización BI", skills_covered={"sql", "excel", "power bi", "tableau"}),
                CurriculumProgram(name="Ingeniería de Datos", skills_covered={"python", "sql", "aws", "docker"})
            ]

    def _get_curriculum(self):
        if self.program_repository:
            return self.program_repository.get_all()
        return self.mock_curriculum

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

    def academic_recommendations(self, source: str, period: str) -> dict:
        try:
            offers = self._load_enriched_offers(source)
            trends = self.trend_service.execute(offers, period)
            forecasts = PredictDemandService(MovingAverageForecastModel()).execute(offers, period, horizon=3)
            recommendations = self.academic_planner.generate_recommendations(trends, forecasts)
            
            return {
                "recommendations": [
                    {
                        "skill_name": r.skill_name,
                        "action": r.action.value,
                        "reason": r.reason,
                        "priority": r.priority,
                        "confidence_score": r.confidence_score,
                        "current_frequency": r.current_frequency,
                        "forecasted_growth": r.forecasted_growth
                    }
                    for r in recommendations
                ]
            }
        except Exception as e:
            print(f"Error in academic_recommendations: {e}")
            return {"recommendations": [], "error": str(e)}

    def gap_analysis(self, source: str, period: str) -> dict:
        try:
            offers = self._load_enriched_offers(source)
            trends = self.trend_service.execute(offers, period)
            curriculum = self._get_curriculum()
            
            alignment_score = self.gap_analyzer.calculate_alignment_index(trends, curriculum)
            gaps = self.gap_analyzer.identify_gaps(trends, curriculum)
            
            return {
                "alignment_score": alignment_score,
                "gaps": [
                    {
                        "skill_name": g.skill_name,
                        "market_demand": g.market_demand,
                        "priority": g.priority,
                        "recommendation": g.recommendation
                    }
                    for g in gaps
                ],
                "curriculum": [
                    {"name": p.name, "skills": list(p.skills_covered)}
                    for p in curriculum
                ]
            }
        except Exception as e:
            print(f"Error in gap_analysis: {e}")
            return {"alignment_score": 0, "gaps": [], "error": str(e)}

    def simulate_syllabus(self, source: str, period: str, added_skills: list[str]) -> dict:
        try:
            offers = self._load_enriched_offers(source)
            trends = self.trend_service.execute(offers, period)
            curriculum = self._get_curriculum()
            
            simulation = self.gap_analyzer.simulate_impact(trends, curriculum, added_skills)
            
            # Generar el reporte Markdown de una vez
            gaps = self.gap_analyzer.identify_gaps(trends, curriculum)
            gaps_data = [
                {
                    "skill_name": g.skill_name,
                    "market_demand": g.market_demand,
                    "priority": g.priority,
                    "recommendation": g.recommendation
                }
                for g in gaps
            ]
            
            report_md = AcademicReportService.generate_markdown_report(simulation, gaps_data, period)
            simulation["report_markdown"] = report_md
            
            return simulation
        except Exception as e:
            print(f"Error in simulate_syllabus: {e}")
            return {"error": str(e)}

    def dashboard_summary(self, source: str, period: str = "monthly") -> dict:
        try:
            offers = self._load_enriched_offers(source)
            trends = self.trend_service.execute(offers, period)
            forecasts = PredictDemandService(MovingAverageForecastModel()).execute(offers, period, horizon=3)
            emerging = self.emerging_service.execute(offers, period, threshold=0.5)
            
            top_skills = sorted(
                [
                    {"skill": trend.skill_name, "frequency": trend.frequency}
                    for trend in trends
                ],
                key=lambda item: item["frequency"],
                reverse=True,
            )
            
            # Consolidate top skills (they might repeat for different periods)
            consolidated: dict[str, int] = {}
            for item in top_skills:
                consolidated[item["skill"]] = consolidated.get(item["skill"], 0) + item["frequency"]
            
            final_top = sorted(
                [{"skill": k, "frequency": v} for k, v in consolidated.items()],
                key=lambda x: x["frequency"],
                reverse=True
            )[:10]

            return {
                "trend_count": len(trends),
                "forecast_count": len(forecasts),
                "emerging_skills": list(set([trend.skill_name for trend in emerging])),
                "top_skills": final_top,
            }
        except Exception as e:
            print(f"Error in dashboard_summary: {e}")
            return {
                "trend_count": 0,
                "forecast_count": 0,
                "emerging_skills": [],
                "top_skills": [],
                "error": str(e)
            }
