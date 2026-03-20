from sqlalchemy.orm import Session
from domain.entities.curriculum import CurriculumProgram
from infrastructure.database.models import ProgramModel
from typing import List

class SQLProgramRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[CurriculumProgram]:
        programs = self.db.query(ProgramModel).all()
        return [
            CurriculumProgram(name=p.name, skills_covered=set(p.skills), description=p.description or "")
            for p in programs
        ]

    def save(self, program: CurriculumProgram):
        db_program = self.db.query(ProgramModel).filter(ProgramModel.name == program.name).first()
        if db_program:
            db_program.skills = list(program.skills_covered)
            db_program.description = program.description
        else:
            db_program = ProgramModel(
                name=program.name,
                skills=list(program.skills_covered),
                description=program.description
            )
            self.db.add(db_program)
        self.db.commit()

    def delete(self, name: str):
        self.db.query(ProgramModel).filter(ProgramModel.name == name).delete()
        self.db.commit()

    def seed_initial_data(self):
        if self.db.query(ProgramModel).count() == 0:
            initial = [
                CurriculumProgram(name="Bootcamp Data Science", skills_covered={"python", "sql", "pandas", "numpy", "scikit-learn"}),
                CurriculumProgram(name="Especialización BI", skills_covered={"sql", "excel", "power bi", "tableau"}),
                CurriculumProgram(name="Ingeniería de Datos", skills_covered={"python", "sql", "aws", "docker"})
            ]
            for p in initial:
                self.save(p)
