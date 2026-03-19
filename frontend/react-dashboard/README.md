# React Dashboard (especificación inicial)

## Vistas sugeridas
- Resumen ejecutivo con KPI cards.
- Tendencias por habilidad y categoría.
- Ranking de habilidades emergentes.
- Comparación entre industrias/regiones.
- Módulo de recomendaciones de cursos.

## Stack sugerido
- React + Vite
- TypeScript
- Plotly.js o Chart.js
- TanStack Query para consumo de API

## Contratos esperados
Consumir:
- `GET /api/v1/dashboard/summary`
- `POST /api/v1/trends/analyze`
- `POST /api/v1/demand/predict`
