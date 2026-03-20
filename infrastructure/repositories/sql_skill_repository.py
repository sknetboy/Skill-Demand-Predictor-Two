from sqlalchemy import create_base
from sqlalchemy.orm import Session
from application.ports.output_ports import SkillRepositoryPort
from domain.entities.skill import Skill
from infrastructure.database.models import SkillModel


class SQLSkillRepository(SkillRepositoryPort):
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def save_skills(self, skills: list[Skill]) -> None:
        for skill in skills:
            db_skill = SkillModel(
                name=skill.name,
                category=skill.category.value if hasattr(skill.category, 'value') else str(skill.category),
                metadata_info=skill.metadata if hasattr(skill, 'metadata') else {}
            )
            self.db_session.add(db_skill)
        self.db_session.commit()
