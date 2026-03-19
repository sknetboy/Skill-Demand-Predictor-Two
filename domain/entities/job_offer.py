from dataclasses import dataclass, field
from datetime import date
from domain.entities.skill import Skill


@dataclass
class JobOffer:
    offer_id: str
    title: str
    description: str
    industry: str
    published_at: date
    company: str
    location: str
    skills: list[Skill] = field(default_factory=list)
