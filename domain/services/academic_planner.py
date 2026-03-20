from typing import List
from domain.entities.trend import Trend
from domain.entities.academic_plan import AcademicRecommendation, RecommendationAction

class AcademicPlannerService:
    def __init__(self, growth_threshold: float = 0.4, frequency_threshold: int = 3, obsolescence_threshold: float = -0.2):
        self.growth_threshold = growth_threshold
        self.frequency_threshold = frequency_threshold
        self.obsolescence_threshold = obsolescence_threshold

    def generate_recommendations(self, historical_trends: List[Trend], forecasts: List[Trend]) -> List[AcademicRecommendation]:
        recommendations = []
        
        # Agrupar tendencias por habilidad para análisis consolidado
        by_skill_hist = {}
        for t in historical_trends:
            if t.skill_name not in by_skill_hist:
                by_skill_hist[t.skill_name] = []
            by_skill_hist[t.skill_name].append(t)
            
        by_skill_forecast = {}
        for t in forecasts:
            if t.skill_name not in by_skill_forecast:
                by_skill_forecast[t.skill_name] = []
            by_skill_forecast[t.skill_name].append(t)

        all_skills = set(list(by_skill_hist.keys()) + list(by_skill_forecast.keys()))

        for skill in all_skills:
            hist_list = by_skill_hist.get(skill, [])
            forecast_list = by_skill_forecast.get(skill, [])
            
            if not hist_list: continue
            
            latest_hist = sorted(hist_list, key=lambda x: x.period)[-1]
            latest_forecast = sorted(forecast_list, key=lambda x: x.period)[-1] if forecast_list else None
            
            # Lógica de decisión académica
            avg_growth = latest_hist.growth_rate
            current_freq = latest_hist.frequency
            forecast_val = latest_forecast.forecast if latest_forecast else current_freq
            
            # 1. Abrir nuevo curso (Alta demanda + Alto crecimiento proyectado)
            if forecast_val > self.frequency_threshold and avg_growth > self.growth_threshold:
                recommendations.append(AcademicRecommendation(
                    skill_name=skill,
                    action=RecommendationAction.OPEN_NEW_COURSE,
                    reason=f"Crecimiento explosivo detectado ({avg_growth:.1%}) con alta demanda proyectada.",
                    priority="Alta",
                    confidence_score=0.85,
                    current_frequency=current_freq,
                    forecasted_growth=avg_growth
                ))
                
            # 2. Lanzar certificación (Demanda estable y alta)
            elif current_freq > self.frequency_threshold * 1.5 and abs(avg_growth) < 0.2:
                recommendations.append(AcademicRecommendation(
                    skill_name=skill,
                    action=RecommendationAction.LAUNCH_CERTIFICATION,
                    reason="Habilidad consolidada con demanda masiva estable en el mercado.",
                    priority="Media",
                    confidence_score=0.9,
                    current_frequency=current_freq,
                    forecasted_growth=avg_growth
                ))

            # 3. Actualizar contenidos (Demanda creciente pero ya existente)
            elif 0.1 < avg_growth <= self.growth_threshold:
                recommendations.append(AcademicRecommendation(
                    skill_name=skill,
                    action=RecommendationAction.UPDATE_CONTENT,
                    reason="Demanda en aumento constante. Actualización de syllabus recomendada.",
                    priority="Media",
                    confidence_score=0.75,
                    current_frequency=current_freq,
                    forecasted_growth=avg_growth
                ))

            # 4. Obsolescencia (Crecimiento negativo sostenido)
            elif avg_growth < self.obsolescence_threshold:
                recommendations.append(AcademicRecommendation(
                    skill_name=skill,
                    action=RecommendationAction.OBSOLETE_WARNING,
                    reason=f"Caída significativa en la demanda ({avg_growth:.1%}). Evaluar retiro gradual.",
                    priority="Alta",
                    confidence_score=0.7,
                    current_frequency=current_freq,
                    forecasted_growth=avg_growth
                ))
            
            # 5. Monitorear (Caso base)
            else:
                recommendations.append(AcademicRecommendation(
                    skill_name=skill,
                    action=RecommendationAction.MONITOR,
                    reason="Demanda estable sin cambios significativos detectados.",
                    priority="Baja",
                    confidence_score=0.6,
                    current_frequency=current_freq,
                    forecasted_growth=avg_growth
                ))

        return sorted(recommendations, key=lambda x: (x.priority == "Alta", x.current_frequency), reverse=True)
