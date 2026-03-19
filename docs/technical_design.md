# Documento técnico: Skill Demand Predictor

## 1. Problema
El mercado laboral cambia rápidamente y las organizaciones necesitan anticipar qué habilidades crecerán para ajustar currículos, rutas de formación, contratación y estrategias de upskilling.

## 2. Objetivo
Construir una plataforma modular que integre analítica descriptiva y predictiva para identificar tendencias de habilidades y estimar demanda futura.

## 3. Decisiones arquitectónicas
- **Hexagonal Architecture** para desacoplar dominio, casos de uso y adaptadores.
- **SOLID** para mantener alta cohesión y extensibilidad.
- **Clean Architecture** para que la lógica de negocio no dependa de frameworks.
- **MLOps-ready** mediante puertos para modelos, ETL y visualización, habilitando sustitución por servicios externos.

## 4. Capas
### Dominio
Entidades (`Skill`, `JobOffer`, `Industry`, `Trend`) y value objects (`SkillCategory`, `TimePeriod`) encapsulan reglas del negocio.

### Aplicación
Los casos de uso orquestan el flujo:
- `ExtractSkillsService`
- `AnalyzeTrendsService`
- `PredictDemandService`
- `DetectEmergingSkillsService`

### Infraestructura
Adaptadores concretos:
- ETL sobre CSV/JSON
- Extractor NLP basado en reglas extensibles a spaCy/BERT
- Modelos intercambiables (`MovingAverageForecastModel`, `RandomForestForecastModel`)
- Visualización para dashboard

### Interfaces
FastAPI expone endpoints REST y `main.py` funciona como CLI para entrenamiento/manual execution.

## 5. Microservicios propuestos
1. **Backend API**: expone vacantes, tendencias y dashboards.
2. **ML Service**: encapsula entrenamiento, evaluación y serving de predicciones.

## 6. Escalabilidad
- Reemplazar repositorios de archivo por PostgreSQL.
- Registrar modelos/versionado en MLflow.
- Automatizar jobs con scheduler/Celery/Airflow.
- Desplegar API y ML service en contenedores separados.
