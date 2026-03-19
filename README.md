# Skill Demand Predictor

Sistema modular para predecir demanda futura de habilidades laborales aplicando Hexagonal Architecture, SOLID, Clean Architecture y prácticas de Data Science/MLOps.

## Capacidades incluidas
- Ingesta y normalización de vacantes desde CSV/JSON.
- Extracción de habilidades técnicas, blandas, herramientas e idiomas.
- Análisis temporal por periodos mensuales o trimestrales.
- Detección de habilidades emergentes mediante crecimiento acelerado.
- Predicción de demanda con modelos intercambiables a través de puertos.
- API REST con FastAPI y documentación Swagger automática.
- Exportación de resultados en JSON/CSV y artefactos para dashboard.

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
