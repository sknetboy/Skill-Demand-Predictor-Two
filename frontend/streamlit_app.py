import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Skill Demand Predictor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo personalizado compatible con ambos temas
st.markdown("""
    <style>
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .stMetric label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

API_BASE_URL = "http://127.0.0.1:8000"

def check_api_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        return response.status_code == 200
    except:
        return False

# Sidebar
st.sidebar.title("🚀 Skill Predictor")
st.sidebar.markdown("---")
source_file = st.sidebar.text_input("Dataset (CSV)", "data/raw/job_offers_sample.csv")
period = st.sidebar.selectbox("Periodo", ["monthly", "quarterly"])
horizon = st.sidebar.slider("Horizonte de Predicción", 1, 12, 3)
model_name = st.sidebar.selectbox("Modelo", ["moving_average", "random_forest"])

st.sidebar.markdown("---")
if st.sidebar.button("Refrescar Datos"):
    st.rerun()

# Main Content
st.title("📊 Dashboard de Demanda de Habilidades")

if not check_api_health():
    st.error(f"❌ No se pudo conectar con la API en {API_BASE_URL}. Asegúrate de que el servidor FastAPI esté corriendo.")
    st.stop()

# Summary Metrics
try:
    summary_resp = requests.get(f"{API_BASE_URL}/api/v1/dashboard/summary", params={"source": source_file, "period": period})
    if summary_resp.status_code == 200:
        summary = summary_resp.json()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tendencias", summary.get("trend_count", 0))
        with col2:
            st.metric("Predicciones", summary.get("forecast_count", 0))
        with col3:
            st.metric("Habilidades Emergentes", len(summary.get("emerging_skills", [])))
            
        # Top Skills Bar Chart
        st.subheader("🔝 Top 10 Habilidades Demandadas")
        top_skills_data = summary.get("top_skills", [])
        if top_skills_data:
            top_skills_df = pd.DataFrame(top_skills_data)
            fig_top = px.bar(
                top_skills_df, 
                x="frequency", 
                y="skill", 
                orientation='h',
                color="frequency",
                color_continuous_scale="Viridis",
                labels={"frequency": "Frecuencia", "skill": "Habilidad"}
            )
            fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_top, use_container_width=True)
        else:
            st.info("No hay datos suficientes para mostrar el ranking de habilidades.")
            
except Exception as e:
    st.warning(f"No se pudieron cargar las métricas de resumen: {e}")

# Detailed Analysis Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Tendencias", "🔮 Predicciones", "✨ Emergentes", "🎓 Planeación Académica"])

with tab1:
    st.subheader("Análisis de Tendencias")
    st.info("💡 Pulsa el botón para cargar el histórico de habilidades.")
    if st.button("Analizar Tendencias"):
        with st.spinner("Procesando..."):
            resp = requests.post(f"{API_BASE_URL}/api/v1/trends/analyze", json={"source": source_file, "period": period})
            if resp.status_code == 200:
                trends_data = resp.json().get("series", [])
                if trends_data:
                    df_trends = pd.DataFrame(trends_data)
                    st.dataframe(df_trends, use_container_width=True)
                    
                    # Line chart for a selected skill
                    selected_skill = st.selectbox("Selecciona una habilidad para ver su evolución", df_trends["skill"].unique())
                    skill_df = df_trends[df_trends["skill"] == selected_skill]
                    fig_skill = px.line(skill_df, x="period", y="frequency", title=f"Evolución de {selected_skill}")
                    st.plotly_chart(fig_skill, use_container_width=True)
                else:
                    st.info("No se encontraron tendencias para el periodo seleccionado.")

with tab2:
    st.subheader("Predicción de Demanda Futura")
    st.info("💡 Usa el control de la izquierda para cambiar el modelo (Random Forest / Moving Average).")
    if st.button("Generar Predicciones"):
        with st.spinner("Entrenando modelos y prediciendo..."):
            resp = requests.post(
                f"{API_BASE_URL}/api/v1/demand/predict", 
                json={"source": source_file, "period": period, "horizon": horizon, "model": model_name}
            )
            if resp.status_code == 200:
                predict_data = resp.json().get("series", [])
                if predict_data:
                    df_predict = pd.DataFrame(predict_data)
                    st.dataframe(df_predict, use_container_width=True)
                    
                    # Visualization of forecast
                    selected_skill_p = st.selectbox("Ver predicción para:", df_predict["skill"].unique())
                    skill_p_df = df_predict[df_predict["skill"] == selected_skill_p]
                    
                    fig_p = go.Figure()
                    fig_p.add_trace(go.Scatter(x=skill_p_df["period"], y=skill_p_df["frequency"], name="Histórico"))
                    fig_p.add_trace(go.Scatter(x=skill_p_df["period"], y=skill_p_df["forecast"], name="Predicción", line=dict(dash='dash', color='red')))
                    fig_p.update_layout(title=f"Predicción de Demanda: {selected_skill_p}", xaxis_title="Periodo", yaxis_title="Frecuencia")
                    st.plotly_chart(fig_p, use_container_width=True)

with tab3:
    st.subheader("Detección de Habilidades Emergentes")
    threshold = st.slider("Umbral de Crecimiento (Growth Rate)", 0.0, 2.0, 0.5)
    if st.button("Detectar"):
        with st.spinner("Buscando nuevas tendencias..."):
            resp = requests.post(
                f"{API_BASE_URL}/api/v1/skills/emerging", 
                json={"source": source_file, "period": period, "threshold": threshold}
            )
            if resp.status_code == 200:
                emerging_data = resp.json().get("series", [])
                if emerging_data:
                    df_emerging = pd.DataFrame(emerging_data)
                    st.success(f"¡Se detectaron {len(df_emerging)} habilidades con alto crecimiento!")
                    
                    # Bubbles chart for emerging skills
                    fig_em = px.scatter(
                        df_emerging, 
                        x="frequency", 
                        y="growth_rate", 
                        size="frequency", 
                        color="skill",
                        hover_name="skill",
                        title="Habilidades Emergentes: Frecuencia vs Tasa de Crecimiento",
                        labels={"frequency": "Frecuencia Actual", "growth_rate": "Tasa de Crecimiento"}
                    )
                    st.plotly_chart(fig_em, use_container_width=True)
                    st.dataframe(df_emerging)
                else:
                    st.info("No se detectaron habilidades que superen el umbral de crecimiento.")

with tab4:
    st.subheader("🎓 Planeación Académica Estratégica")
    st.markdown("""
        Esta sección permite alinear la oferta educativa con las necesidades reales del mercado laboral, 
        identificando brechas en el currículo actual y sugiriendo acciones estratégicas.
    """)
    
    # Análisis de Brechas (Gap Analysis)
    st.markdown("### 🔍 Análisis de Brechas (Market vs Curriculum)")
    if st.button("Realizar Gap Analysis"):
        with st.spinner("Comparando currículo con demanda del mercado..."):
            gap_resp = requests.get(
                f"{API_BASE_URL}/api/v1/academic/gap-analysis", 
                params={"source": source_file, "period": period}
            )
            if gap_resp.status_code == 200:
                gap_data = gap_resp.json()
                alignment = gap_data.get("alignment_score", 0)
                
                # Gauge chart para Alineación
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = alignment,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Índice de Alineación Curricular (%)"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#00cc96"},
                        'steps': [
                            {'range': [0, 50], 'color': "#ef553b"},
                            {'range': [50, 80], 'color': "#fecb52"},
                            {'range': [80, 100], 'color': "#00cc96"}
                        ],
                    }
                ))
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                if alignment < 70:
                    st.warning(f"⚠️ Tu currículo tiene una alineación baja ({alignment:.1f}%). Se recomienda revisar las brechas críticas.")
                else:
                    st.success(f"✅ ¡Excelente! Tu currículo está bien alineado ({alignment:.1f}%) con el mercado.")

                # Tabla de Gaps
                gaps = gap_data.get("gaps", [])
                if gaps:
                    st.markdown("#### 🚩 Brechas Detectadas (Habilidades no cubiertas)")
                    df_gaps = pd.DataFrame(gaps)
                    st.dataframe(df_gaps, use_container_width=True)
                
                # Mostrar currículo actual
                with st.expander("Ver Programas Académicos Actuales"):
                    for prog in gap_data.get("curriculum", []):
                        st.write(f"**{prog['name']}**")
                        st.caption(f"Habilidades: {', '.join(prog['skills'])}")

    st.markdown("---")
    st.markdown("### 🧪 Simulador de Syllabus (Análisis What-if)")
    st.write("Selecciona habilidades que te gustaría añadir a tus programas para ver cómo mejoraría tu alineación con el mercado.")
    
    # Obtener todas las habilidades únicas del mercado para el simulador
    market_skills_list = []
    try:
        resp_trends = requests.post(f"{API_BASE_URL}/api/v1/trends/analyze", json={"source": source_file, "period": period})
        if resp_trends.status_code == 200:
            market_skills_list = sorted([s["skill"] for s in resp_trends.json().get("series", [])])
    except: pass

    selected_to_add = st.multiselect("Habilidades a integrar:", market_skills_list)
    
    if st.button("Simular Impacto"):
        with st.spinner("Simulando mejora curricular..."):
            sim_resp = requests.post(
                f"{API_BASE_URL}/api/v1/academic/simulate",
                json={"source": source_file, "period": period, "added_skills": selected_to_add}
            )
            if sim_resp.status_code == 200:
                sim_result = sim_resp.json()
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Alineación Inicial", f"{sim_result['initial_alignment']:.1f}%")
                c2.metric("Alineación Simulada", f"{sim_result['simulated_alignment']:.1f}%", f"+{sim_result['improvement']:.1f}%")
                c3.metric("Mejora Total", f"{sim_result['improvement']:.1f}%")
                
                if sim_result['improvement'] > 0:
                    st.success(f"🚀 Integrar estas {len(selected_to_add)} habilidades aumentaría tu relevancia en el mercado un {sim_result['improvement']:.1f}%.")
                    
                    # Generar texto de justificación
                    st.markdown("#### 📝 Justificación para el Director Académico")
                    justification = f"""
                    **Propuesta de actualización de Syllabus**
                    
                    Basado en el análisis de {len(selected_to_add)} nuevas competencias ({', '.join(selected_to_add)}), 
                    se ha detectado que su inclusión en los programas académicos actuales elevaría el índice de alineación 
                    con el mercado laboral real del **{sim_result['initial_alignment']:.1f}%** al **{sim_result['simulated_alignment']:.1f}%**.
                    
                    Esta decisión está respaldada por datos de vacantes reales analizados en el periodo {period}, 
                    donde estas habilidades presentan una demanda creciente y una brecha crítica de cobertura.

                    **Habilidades a integrar:** {', '.join(selected_to_add)}
                    
                    *Nota: Este reporte ha sido generado por el sistema de planeación académica basándose en datos reales del mercado.*
                    """
                    st.info(justification)
                    
                    # Botón de descarga del reporte completo
                    st.download_button(
                        label="📥 Descargar Informe de Justificación (Markdown)",
                        data=sim_result.get("report_markdown", ""),
                        file_name=f"informe_academico_{period}.md",
                        mime="text/markdown"
                    )
                else:
                    st.info("Selecciona habilidades del mercado que no estén en tu currículo para ver el impacto.")

    st.markdown("---")
    st.markdown("### 💡 Recomendaciones de Acción")
    if st.button("Generar Plan Académico"):
        with st.spinner("Analizando brechas y oportunidades..."):
            resp = requests.get(
                f"{API_BASE_URL}/api/v1/academic/recommendations", 
                params={"source": source_file, "period": period}
            )
            if resp.status_code == 200:
                recs = resp.json().get("recommendations", [])
                if recs:
                    df_recs = pd.DataFrame(recs)
                    
                    # KPIs rápidos
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        new_courses = len(df_recs[df_recs["action"] == "Abrir nuevo curso"])
                        st.success(f"🆕 {new_courses} Nuevos Cursos")
                    with col_b:
                        updates = len(df_recs[df_recs["action"] == "Actualizar contenidos"])
                        st.info(f"🔄 {updates} Actualizaciones")
                    with col_c:
                        obsolete = len(df_recs[df_recs["action"] == "Posible obsolescencia"])
                        st.warning(f"⚠️ {obsolete} Obsolescencias")

                    # Tabla detallada con colores por prioridad
                    def color_priority(val):
                        color = 'red' if val == 'Alta' else 'orange' if val == 'Media' else 'green'
                        return f'color: {color}; font-weight: bold'

                    st.markdown("### Detalle de Recomendaciones")
                    st.dataframe(
                        df_recs.style.applymap(color_priority, subset=['priority']),
                        use_container_width=True
                    )
                    
                    # Gráfico de Radar o Distribución de Acciones
                    st.markdown("### Distribución de Decisiones Académicas")
                    action_counts = df_recs["action"].value_counts().reset_index()
                    action_counts.columns = ["Acción", "Cantidad"]
                    fig_actions = px.pie(action_counts, values="Cantidad", names="Acción", hole=0.4,
                                        color_discrete_sequence=px.colors.qualitative.Pastel)
                    st.plotly_chart(fig_actions, use_container_width=True)
                    
                else:
                    st.info("No hay suficientes datos para generar recomendaciones académicas.")

# Footer
st.markdown("---")
st.markdown("© 2026 Skill Demand Predictor - Arquitectura Hexagonal & ML")
