from domain.value_objects.skill_category import SkillCategory


class SkillClassifier:
    TECHNICAL = {"python", "sql", "tensorflow", "pandas", "scikit-learn", "machine learning", "aws", "docker"}
    SOFT = {"leadership", "communication", "teamwork", "problem solving", "adaptability"}
    TOOLS = {"jira", "tableau", "power bi", "excel", "git", "kubernetes"}
    LANGUAGES = {"english", "spanish", "french", "german"}

    def classify(self, raw_skill: str) -> SkillCategory:
        normalized = raw_skill.strip().lower()
        if normalized in self.TECHNICAL:
            return SkillCategory.TECHNICAL
        if normalized in self.SOFT:
            return SkillCategory.SOFT
        if normalized in self.TOOLS:
            return SkillCategory.TOOL
        if normalized in self.LANGUAGES:
            return SkillCategory.LANGUAGE
        return SkillCategory.UNKNOWN
