from application.ports.input_ports import ExtractSkillsUseCase
from application.ports.output_ports import SkillRepositoryPort
from domain.entities.job_offer import JobOffer
from infrastructure.nlp.skill_extractor import SkillExtractor


class ExtractSkillsService(ExtractSkillsUseCase):
    def __init__(self, extractor: SkillExtractor, skill_repository: SkillRepositoryPort) -> None:
        self.extractor = extractor
        self.skill_repository = skill_repository

    def execute(self, job_offers: list[JobOffer]) -> list[JobOffer]:
        for offer in job_offers:
            offer.skills = self.extractor.extract(f"{offer.title}. {offer.description}")
            self.skill_repository.save_skills(offer.skills)
        return job_offers
