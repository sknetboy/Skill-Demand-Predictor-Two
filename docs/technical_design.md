# Documento técnico: Skill Demand Predictor

## 1. Problema
El mercado laboral cambia rápidamente y las organizaciones necesitan anticipar qué habilidades crecerán para ajustar currículos, rutas de formación, contratación y estrategias de upskilling.

## 2. Objetivo
Construir una plataforma modular que integre analítica descriptiva y predictiva para identificar tendencias de habilidades y estimar demanda futura.

## 3. Vertical de MVP priorizada
La vertical recomendada para el MVP es un **sistema de planeación académica** para **universidades, bootcamps y empresas edtech**.

### Decisiones que soporta
- Apertura de nuevos cursos y electives.
- Actualización de contenidos, sílabos y rutas de aprendizaje.
- Lanzamiento de certificaciones enfocadas en skills con crecimiento sostenido.
- Identificación de programas, módulos o stacks que están quedando obsoletos.

### Justificación de negocio
- Existe un ajuste natural con el problema original del proyecto, que ya menciona currículos y formación.
- La propuesta de valor es entendible y accionable para equipos académicos, product managers de edtech y directores de bootcamps.
- La venta y validación de un MVP es más simple en este segmento que en un contexto enterprise de gran escala.

### Escenario de referencia
Un bootcamp de data/AI puede detectar crecimiento en skills como **Python, SQL, AWS, Docker, Kubernetes y Power BI** y usar esa señal para rediseñar su oferta formativa.

## 4. Decisiones arquitectónicas
- **Hexagonal Architecture** para desacoplar dominio, casos de uso y adaptadores.
- **SOLID** para mantener alta cohesión y extensibilidad.
- **Clean Architecture** para que la lógica de negocio no dependa de frameworks.
- **MLOps-ready** mediante puertos para modelos, ETL y visualización, habilitando sustitución por servicios externos.

## 5. Capas
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

## 6. Traducción funcional para la vertical académica
- **Extracción de habilidades**: identifica skills demandadas por el mercado para traducirlas a outcomes de aprendizaje.
- **Análisis de tendencias**: muestra qué tecnologías crecen o se desaceleran por periodo.
- **Forecast de demanda**: ayuda a priorizar actualizaciones curriculares con horizonte de mediano plazo.
- **Dashboard**: resume señales para comités académicos o equipos de producto educativo.

## 7. Microservicios propuestos
1. **Backend API**: expone vacantes, tendencias y dashboards.
2. **ML Service**: encapsula entrenamiento, evaluación y serving de predicciones.

## 8. Escalabilidad
- Reemplazar repositorios de archivo por PostgreSQL.
- Registrar modelos/versionado en MLflow.
- Automatizar jobs con scheduler/Celery/Airflow.
- Desplegar API y ML service en contenedores separados.
