# Documentación Técnica - Skill Demand Predictor & Academic Planner

Este documento detalla todos los pasos y componentes implementados en el proyecto para transformar una API de predicción de habilidades en una herramienta integral de planeación académica estratégica.

## 1. Configuración del Entorno y Base de Datos
- **Entorno Virtual**: Se configuró un entorno `venv/` con Python 3.11+.
- **PostgreSQL**: Integración con SQLAlchemy para persistencia de datos reales.
- **Seguridad**: Gestión de credenciales mediante `.env` con codificación de caracteres especiales para URLs de conexión.

## 2. Arquitectura del Proyecto (Hexagonal)
El proyecto sigue una arquitectura limpia que separa las reglas de negocio de los detalles técnicos:
- **Domain**: Entidades núcleo como `Skill`, `Trend`, `JobOffer`, `AcademicRecommendation` y `CurriculumProgram`.
- **Application**: Servicios de lógica de negocio (Use Cases) para extracción, predicción y análisis de tendencias.
- **Infrastructure**: Implementaciones de base de datos (PostgreSQL), ML (Random Forest, Moving Average), y ETL para archivos CSV/JSON.
- **Interfaces**: API REST con FastAPI y Controladores para orquestar la comunicación.

## 3. Motor de Inteligencia y Análisis
- **Extracción de Skills**: Uso de NLP basado en patrones para identificar habilidades técnicas y blandas en descripciones de empleo.
- **Predicción de Demanda**: Modelos de Machine Learning para proyectar la frecuencia de habilidades en el futuro (1-12 meses).
- **Gap Analysis**: Comparación algorítmica entre la demanda del mercado y el currículo actual de la institución.
- **Simulador What-if**: Motor que permite predecir el impacto de añadir nuevas habilidades al syllabus en el índice de alineación curricular.

## 4. Interfaz de Usuario (Dashboard)
Desarrollado con **Streamlit** y visualizaciones de **Plotly**:
- **Pestaña Tendencias**: Visualización histórica de habilidades.
- **Pestaña Predicciones**: Configuración de modelos de ML y horizontes de tiempo.
- **Pestaña Emergentes**: Detección de tecnologías con crecimiento acelerado.
- **Pestaña Académica**: Herramientas exclusivas para directores (Gap Analysis, Simulador de Syllabus y Exportación de Informes).

## 5. Sistema de Reportes
- Generación automática de informes en **Markdown** con KPIs de alineación, justificación técnica y recomendaciones prioritarias.
- Funcionalidad de descarga directa desde la web para uso administrativo.
