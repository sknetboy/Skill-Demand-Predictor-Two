from datetime import datetime
from typing import List, Dict

class AcademicReportService:
    @staticmethod
    def generate_markdown_report(simulation_data: Dict, gaps: List[Dict], period: str) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = f"""# Informe de Justificación Estratégica Académica
*Fecha de generación: {now}*
*Periodo analizado: {period}*

## 1. Resumen Ejecutivo
Este informe presenta una propuesta formal para la actualización de los currículos académicos basada en datos reales del mercado laboral. El objetivo es maximizar la empleabilidad de los egresados alineando el syllabus con las competencias más demandadas.

### KPIs de Impacto Curricular
- **Índice de Alineación Inicial:** {simulation_data['initial_alignment']:.1f}%
- **Índice de Alineación Proyectado:** {simulation_data['simulated_alignment']:.1f}%
- **Incremento en Relevancia de Mercado:** **+{simulation_data['improvement']:.1f}%**

---

## 2. Propuesta de Actualización
Se recomienda la integración inmediata de las siguientes competencias en los programas académicos:

**Habilidades a integrar:**
{", ".join([f"`{s}`" for s in simulation_data['added_skills']])}

### Justificación Técnica
La inclusión de estas competencias responde a una brecha crítica detectada entre la oferta educativa actual y las vacantes reales analizadas. La implementación de estos cambios elevaría la competitividad institucional y aseguraría que los programas sigan siendo relevantes frente a la evolución tecnológica.

---

## 3. Análisis de Brechas Críticas (Gaps)
A continuación se detallan las habilidades que presentan mayor demanda y que actualmente no están cubiertas:

| Habilidad | Demanda (Frecuencia) | Prioridad | Recomendación |
| :--- | :---: | :---: | :--- |
"""
        for g in gaps[:10]: # Top 10 gaps
            report += f"| {g['skill_name']} | {g['market_demand']} | {g['priority']} | {g['recommendation']} |\n"

        report += """
---
## 4. Conclusión
Basado en los datos presentados, la actualización del syllabus no es solo una mejora académica, sino una necesidad estratégica para mantener el liderazgo en la formación de talento técnico.

**Firma:**
*Sistema Automático de Planeación Académica - Skill Demand Predictor*
"""
        return report
