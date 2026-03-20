# Skill Demand Predictor

Sistema modular para predecir demanda futura de habilidades laborales aplicando Hexagonal Architecture, SOLID, Clean Architecture y prácticas de Data Science/MLOps.

## Enfoque de MVP elegido
La propuesta prioritaria es la **Opción C: Sistema de planeación académica para universidad, bootcamp o edtech**.

### Qué resuelve
Ayuda a decidir:
- qué cursos abrir,
- qué contenidos actualizar,
- qué certificaciones lanzar,
- qué programas están quedando obsoletos.

### Por qué tiene buen encaje con este proyecto
- El problema original del proyecto ya contempla el ajuste de currículos y rutas de formación.
- El extractor actual reconoce habilidades muy comunes en programas de data/AI como Python, SQL, AWS, Docker, Kubernetes y Power BI.
- El valor de negocio es claro para instituciones educativas que necesitan alinear rápidamente su oferta con la demanda del mercado.
- Comercialmente, un MVP orientado a edtech o bootcamps es más fácil de validar que una suite enterprise para grandes corporativos.

### Ejemplo de uso realista
Un bootcamp de data/AI puede monitorear crecimiento y forecast de skills como **Python, SQL, AWS, Docker, Kubernetes y Power BI** para:
- abrir nuevos módulos o electives,
- actualizar contenidos del syllabus,
- priorizar certificaciones complementarias,
- retirar programas cuyo stack esté perdiendo relevancia.

## Capacidades incluidas
- Ingesta y normalización de vacantes desde CSV/JSON.
- Extracción de habilidades técnicas, blandas, herramientas e idiomas.
- Análisis temporal por periodos mensuales o trimestrales.
- Detección de habilidades emergentes mediante crecimiento acelerado.
- Predicción de demanda con modelos intercambiables a través de puertos.
- API REST con FastAPI y documentación Swagger automática.
- Exportación de resultados en JSON/CSV y artefactos para dashboard.

## Casos de uso priorizados para la vertical académica
- Detectar qué skills están ganando demanda para abrir nuevos cursos.
- Identificar contenidos que deben actualizarse dentro de un programa vigente.
- Sustentar el lanzamiento de certificaciones cortas basadas en señales del mercado.
- Detectar programas o tracks tecnológicos que muestran señales de obsolescencia.

## Arquitectura
- `domain/`: entidades, value objects y servicios puros.
- `application/`: casos de uso y puertos de entrada/salida.
- `infrastructure/`: adaptadores para ETL, NLP, ML, repositorios y persistencia.
- `interfaces/`: API REST, DTOs y controladores.
- `frontend/react-dashboard/`: especificación inicial para dashboard React.

## Ejecución rápida
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn interfaces.api.main:app --reload
```

## CLI de entrenamiento
```bash
python main.py train --input data/raw/job_offers_sample.csv --period monthly
```

## Endpoints principales
- `POST /api/v1/skills/extract`
- `POST /api/v1/trends/analyze`
- `POST /api/v1/demand/predict`
- `POST /api/v1/skills/emerging`
- `GET /api/v1/dashboard/summary`

## Documentación adicional
- `docs/technical_design.md`
- `docs/ml_pipeline.md`
