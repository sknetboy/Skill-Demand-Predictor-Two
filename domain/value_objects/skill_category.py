from enum import Enum


class SkillCategory(str, Enum):
    TECHNICAL = "technical"
    SOFT = "soft"
    TOOL = "tool"
    LANGUAGE = "language"
    UNKNOWN = "unknown"
