# Skill Demand Predictor & Academic Planner 🎓📈

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/sknetboy/Skill-Demand-Predictor-Two)

Sistema modular para predecir la demanda futura de habilidades laborales y optimizar planes académicos (Syllabus), aplicando Arquitectura Hexagonal, SOLID, Clean Architecture y Data Science.

## 🚀 Capacidades Principales
- **Análisis de Mercado**: Ingesta y normalización de vacantes desde CSV/JSON.
- **Extracción de Skills**: Identificación de habilidades técnicas, blandas e idiomas mediante NLP.
- **Predicción con ML**: Pronóstico de demanda futura usando Random Forest y Medias Móviles.
- **Planeación Académica Estratégica**:
  - **Gap Analysis**: Compara el currículo actual con la demanda real del mercado.
  - **Simulador de Syllabus**: Mide el impacto de añadir nuevas habilidades antes de implementarlas.
  - **Informes de Justificación**: Generación y descarga de reportes automáticos para directores académicos.
- **Dashboard Interactivo**: Interfaz visual completa desarrollada en Streamlit con gráficos de Plotly.

## 🛠️ Arquitectura
- `domain/`: Entidades, value objects y lógica de negocio pura.
- `application/`: Casos de uso y puertos de entrada/salida.
- `infrastructure/`: Adaptadores para PostgreSQL, ETL, NLP y modelos de ML.
- `interfaces/`: API REST (FastAPI), DTOs y controladores.
- `frontend/`: Dashboard interactivo de Streamlit.

## 📥 Instalación Rápida
1. Crear entorno virtual: `python -m venv venv`
2. Activar entorno: `.\venv\Scripts\activate` (Windows)
3. Instalar dependencias: `pip install -r requirements.txt` (o `pip install .`)
4. Configurar `.env` con tus credenciales de PostgreSQL.

## 🚦 Ejecución
- **Servidor API (Backend)**:
  ```bash
  uvicorn interfaces.api.main:app --reload
  ```
- **Dashboard (Frontend)**:
  ```bash
  streamlit run frontend/streamlit_app.py
  ```

## 📚 Documentación Adicional
- [docs.md](docs.md): Documentación técnica detallada de los pasos implementados.
- [README_GUIA_RAPIDA.md](README_GUIA_RAPIDA.md): Guía simplificada para no programadores.
