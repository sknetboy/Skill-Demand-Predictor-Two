from typing import List, Dict
from domain.entities.trend import Trend
from domain.entities.curriculum import CurriculumProgram, CurriculumGap

class GapAnalyzerService:
    def __init__(self, high_demand_threshold: int = 5):
        self.high_demand_threshold = high_demand_threshold

    def calculate_alignment_index(self, market_trends: List[Trend], current_curriculum: List[CurriculumProgram]) -> float:
        """Calcula un porcentaje de 0 a 100 de qué tan alineado está el currículo con el mercado."""
        covered_skills = set()
        for program in current_curriculum:
            covered_skills.update([s.lower() for s in program.skills_covered])
            
        market_skills = {}
        for trend in market_trends:
            market_skills[trend.skill_name.lower()] = market_skills.get(trend.skill_name.lower(), 0) + trend.frequency
            
        if not market_skills:
            return 100.0
            
        weighted_coverage = 0
        total_market_weight = sum(market_skills.values())
        
        for skill, frequency in market_skills.items():
            if skill in covered_skills:
                weighted_coverage += frequency
                
        return (weighted_coverage / total_market_weight) * 100 if total_market_weight > 0 else 100.0

    def identify_gaps(self, market_trends: List[Trend], current_curriculum: List[CurriculumProgram]) -> List[CurriculumGap]:
        covered_skills = set()
        for program in current_curriculum:
            covered_skills.update([s.lower() for s in program.skills_covered])
            
        market_demand: Dict[str, int] = {}
        for trend in market_trends:
            market_demand[trend.skill_name.lower()] = market_demand.get(trend.skill_name.lower(), 0) + trend.frequency
            
        gaps = []
        for skill, demand in market_demand.items():
            coverage = 1.0 if skill in covered_skills else 0.0
            
            if coverage < 1.0:
                priority = "Crítica" if demand >= self.high_demand_threshold else "Alta" if demand >= self.high_demand_threshold / 2 else "Media"
                gaps.append(CurriculumGap(
                    skill_name=skill,
                    market_demand=demand,
                    curriculum_coverage=coverage,
                    priority=priority,
                    recommendation=f"Integrar módulo de {skill} en programas existentes o abrir seminario intensivo."
                ))
                
        return sorted(gaps, key=lambda x: x.market_demand, reverse=True)

    def simulate_impact(self, market_trends: List[Trend], current_curriculum: List[CurriculumProgram], added_skills: List[str]) -> dict:
        """Simula el impacto de añadir nuevas habilidades al currículo."""
        # Currículo actual
        initial_score = self.calculate_alignment_index(market_trends, current_curriculum)
        
        # Currículo simulado
        simulated_curriculum = []
        for p in current_curriculum:
            simulated_curriculum.append(CurriculumProgram(
                name=p.name,
                skills_covered=p.skills_covered.union(set(added_skills)),
                description=p.description
            ))
            
        final_score = self.calculate_alignment_index(market_trends, simulated_curriculum)
        
        return {
            "initial_alignment": initial_score,
            "simulated_alignment": final_score,
            "improvement": final_score - initial_score,
            "added_skills": added_skills
        }
