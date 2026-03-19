import re
from collections import Counter
from domain.entities.skill import Skill
from domain.services.skill_classifier import SkillClassifier


class SkillExtractor:
    def __init__(self, classifier: SkillClassifier | None = None) -> None:
        self.classifier = classifier or SkillClassifier()
        self.patterns = [
            r"python", r"sql", r"tensorflow", r"pandas", r"scikit-learn", r"machine learning",
            r"aws", r"docker", r"kubernetes", r"tableau", r"power bi", r"excel", r"git",
            r"leadership", r"communication", r"teamwork", r"problem solving", r"adaptability",
            r"english", r"spanish", r"french", r"german"
        ]

    def extract(self, text: str) -> list[Skill]:
        normalized = text.lower()
        matches: list[str] = []
        for pattern in self.patterns:
            matches.extend(re.findall(pattern, normalized))
        counted = Counter(matches)
        return [
            Skill(name=name, category=self.classifier.classify(name), occurrences=count)
            for name, count in counted.items()
        ]
