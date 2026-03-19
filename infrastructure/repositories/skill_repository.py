from application.ports.output_ports import SkillRepositoryPort
from domain.entities.skill import Skill


class InMemorySkillRepository(SkillRepositoryPort):
    def __init__(self) -> None:
        self.items: list[Skill] = []

    def save_skills(self, skills: list[Skill]) -> None:
        self.items.extend(skills)
