import argparse
from application.use_cases.detect_emerging_skills import DetectEmergingSkillsService
from application.use_cases.extract_skills import ExtractSkillsService
from application.use_cases.predict_demand import PredictDemandService
from infrastructure.ml.models import MovingAverageForecastModel, RandomForestForecastModel
from infrastructure.nlp.skill_extractor import SkillExtractor
from infrastructure.repositories.job_data_repository import FileJobDataRepository
from infrastructure.repositories.skill_repository import InMemorySkillRepository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Skill Demand Predictor CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train = subparsers.add_parser("train", help="Ejecuta extracción y predicción")
    train.add_argument("--input", required=True)
    train.add_argument("--period", default="monthly", choices=["monthly", "quarterly"])
    train.add_argument("--horizon", type=int, default=3)
    train.add_argument("--model", default="moving_average", choices=["moving_average", "random_forest"])

    emerging = subparsers.add_parser("emerging", help="Detecta habilidades emergentes")
    emerging.add_argument("--input", required=True)
    emerging.add_argument("--period", default="monthly", choices=["monthly", "quarterly"])
    emerging.add_argument("--threshold", type=float, default=0.5)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    job_repository = FileJobDataRepository()
    skill_repository = InMemorySkillRepository()
    extractor = ExtractSkillsService(SkillExtractor(), skill_repository)
    offers = extractor.execute(job_repository.load_job_offers(args.input))

    if args.command == "train":
        model = RandomForestForecastModel() if args.model == "random_forest" else MovingAverageForecastModel()
        forecast = PredictDemandService(model).execute(offers, args.period, args.horizon)
        for item in forecast:
            print(f"{item.skill_name},{item.period},{item.frequency},{item.forecast}")
    elif args.command == "emerging":
        emerging = DetectEmergingSkillsService().execute(offers, args.period, args.threshold)
        for item in emerging:
            print(f"{item.skill_name},{item.period},{item.frequency},{item.growth_rate}")


if __name__ == "__main__":
    main()
