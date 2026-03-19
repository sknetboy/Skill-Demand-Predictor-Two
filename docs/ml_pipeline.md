# Pipeline de Data Science y MLOps

## 1. Ingesta
- Entrada desde CSV/JSON o APIs reales de empleo.
- Validación de columnas obligatorias.
- Eliminación de duplicados por `offer_id`.

## 2. Preprocesamiento
- Limpieza básica de texto y normalización de espacios.
- Conversión de fechas.
- Punto de extensión para tokenización, lematización y embeddings.

## 3. Extracción de habilidades
- Enfoque inicial rule-based.
- Clasificación automática por categoría: técnica, blanda, herramienta, idioma.
- Extensible a NER con spaCy/BERT.

## 4. Análisis temporal
- Agrupación mensual o trimestral.
- Cálculo de frecuencia y tasa de crecimiento.
- Detección de crecimiento acelerado con umbral configurable.

## 5. Modelado
- `MovingAverageForecastModel` como baseline interpretable.
- `RandomForestForecastModel` como alternativa no lineal.
- Puertos preparados para integrar Prophet, ARIMA o LSTM.

## 6. Evaluación
- Métricas implementadas: MAE, RMSE, MAPE.
- Se recomienda añadir validación cruzada temporal, backtesting y SHAP en siguientes iteraciones.

## 7. Operación
- Registrar datasets y métricas.
- Versionar modelos.
- Automatizar reentrenamiento y monitoreo de drift.
