from collections import defaultdict
from domain.entities.job_offer import JobOffer
from domain.entities.trend import Trend
from domain.value_objects.skill_category import SkillCategory


class TrendAnalyzer:
    def calculate_trends(self, job_offers: list[JobOffer], period_labels: list[str]) -> list[Trend]:
        frequencies: dict[tuple[str, str], int] = defaultdict(int)
        categories: dict[str, SkillCategory] = {}

        for offer, period_label in zip(job_offers, period_labels):
            for skill in offer.skills:
                frequencies[(skill.name.lower(), period_label)] += 1
                categories[skill.name.lower()] = skill.category

        grouped_by_skill: dict[str, list[tuple[str, int]]] = defaultdict(list)
        for (skill_name, period), frequency in frequencies.items():
            grouped_by_skill[skill_name].append((period, frequency))

        trends: list[Trend] = []
        for skill_name, values in grouped_by_skill.items():
            previous = 0
            for period, frequency in sorted(values, key=lambda item: item[0]):
                growth_rate = 0.0 if previous == 0 else (frequency - previous) / previous
                trends.append(
                    Trend(
                        skill_name=skill_name,
                        category=categories.get(skill_name, SkillCategory.UNKNOWN),
                        period=period,
                        frequency=frequency,
                        growth_rate=growth_rate,
                    )
                )
                previous = frequency
        return trends

    def detect_accelerated_growth(self, trends: list[Trend], threshold: float = 0.5) -> list[Trend]:
        return [trend for trend in trends if trend.growth_rate >= threshold and trend.frequency >= 2]
