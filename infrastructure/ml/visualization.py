from application.ports.output_ports import VisualizationPort
from domain.entities.trend import Trend


class PlotlyVisualizationAdapter(VisualizationPort):
    def build_skill_trends(self, trends: list[Trend]) -> dict:
        return {
            "series": [
                {
                    "skill": trend.skill_name,
                    "period": trend.period,
                    "frequency": trend.frequency,
                    "growth_rate": trend.growth_rate,
                    "forecast": trend.forecast,
                    "emerging": trend.emerging,
                }
                for trend in trends
            ]
        }
