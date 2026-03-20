# 🎓 Guía Rápida: Skill Demand Predictor & Academic Planner

**Repositorio oficial:** [https://github.com/sknetboy/Skill-Demand-Predictor-Two](https://github.com/sknetboy/Skill-Demand-Predictor-Two)

Esta guía está diseñada para que cualquier persona, sin necesidad de conocimientos avanzados en programación, pueda ejecutar el proyecto y visualizar los datos académicos de forma sencilla.

## 🏁 Pasos para Ejecutar el Proyecto (Windows)

1. **Abrir una terminal**: En la carpeta del proyecto, escribe `cmd` o `powershell` en la barra de direcciones de la carpeta.
2. **Activar el entorno**:
   ```powershell
   .\venv\Scripts\activate
   ```
3. **Iniciar la Aplicación**:
   Debes ejecutar dos comandos en terminales diferentes (o uno tras otro):
   
   - **Terminal 1 (Backend)**:
     ```powershell
     uvicorn interfaces.api.main:app --reload
     ```
   - **Terminal 2 (Interfaz Gráfica)**:
     ```powershell
     streamlit run frontend/streamlit_app.py
     ```
4. **Ver el Dashboard**: Se abrirá automáticamente una pestaña en tu navegador en `http://127.0.0.1:8501`.

---

## ☁️ Cómo actualizar el repositorio en GitHub

Si has hecho cambios y quieres guardarlos en tu cuenta de GitHub, sigue estos pasos:

1. **Ver qué cambios hay**:
   ```bash
   git status
   ```
2. **Añadir todos los cambios**:
   ```bash
   git add .
   ```
3. **Guardar los cambios (Commit)**: Escribe una breve descripción de lo que hiciste.
   ```bash
   git commit -m "Actualización: Mejora de interfaz académica y reportes"
   ```
4. **Subir a la nube (Push)**:
   ```bash
   git push origin main
   ```

---

## 📊 ¿Cómo usar el Dashboard Académico?

1. Ve a la pestaña **🎓 Planeación Académica**.
2. **Gap Analysis**: Pulsa el botón "Realizar Gap Analysis" para ver qué habilidades le faltan a tu currículo según el mercado actual.
3. **Simulador**: Selecciona habilidades de la lista y pulsa "Simular Impacto" para ver cuánto mejoraría tu programa académico.
4. **Descargar Informe**: Una vez hecha la simulación, usa el botón "Descargar Informe" para obtener un archivo listo para presentar en reuniones académicas.

---
© 2026 Skill Demand Predictor - Herramienta Estratégica para EdTech e Instituciones.
