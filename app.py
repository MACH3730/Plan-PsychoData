import streamlit as st
import pandas as pd
import numpy as np
from logic import (
    limpiar_datos, 
    es_dicotomico, 
    procesar_y_ordenar_items, 
    calcular_alfa_cronbach, 
    calcular_fiabilidad_mitades,
    preparar_datos_grafico
)

st.set_page_config(page_title="PsychoData Engine v2", layout="wide")
st.title("🧠 Plan PsychoData: Análisis Psicométrico Profesional")

with st.sidebar:
    st.header("⚙️ Configuración")
    uploaded_file = st.file_uploader("Carga tu archivo CSV", type="csv")
    metodo_mitades = st.radio("Fórmula de Dos Mitades:", ["spearman_brown", "rulon"])
    opcion_nulos = st.radio("Gestión de nulos:", ["Eliminar sujeto", "Sustituir por 0"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    df_clean = limpiar_datos(df_raw, metodo=opcion_nulos)
    df_analisis = procesar_y_ordenar_items(df_clean)
    
    # Métricas principales
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Consistencia Interna", value=f"{calcular_alfa_cronbach(df_analisis):.4f}")
    with col2:
        st.metric(label=f"Fiabilidad {metodo_mitades.upper()}", value=f"{calcular_fiabilidad_mitades(df_analisis, metodo=metodo_mitades.lower()):.4f}")

    # --- SECCIÓN DE ANÁLISIS VISUAL INDIVIDUAL ---
    st.markdown("---")
    st.subheader("🎯 Análisis Visual Detallado")
    
    col_sel1, col_sel2 = st.columns(2)
    
    with col_sel1:
        modo = st.selectbox("¿Qué deseas analizar?", ["Un Sujeto específico", "Un Ítem específico"])
    
    df_graf = preparar_datos_grafico(df_analisis)

    with col_sel2:
        if modo == "Un Sujeto específico":
            # El usuario elige un ID de la lista disponible
            seleccion = st.selectbox("Selecciona el ID del sujeto:", df_graf.index.unique())
        else:
            # El usuario elige una columna (V1, V2...)
            seleccion = st.selectbox("Selecciona el Ítem:", df_graf.columns)

    # Renderizado del gráfico individual
    if modo == "Un Sujeto específico":
        data_to_plot = df_graf.loc[seleccion]
        st.line_chart(data_to_plot)
        st.caption(f"Trayectoria del Sujeto {seleccion} a través de los ítems (ordenados por dificultad p).")
    else:
        data_to_plot = df_graf[seleccion]
        st.line_chart(data_to_plot)
        st.caption(f"Rendimiento del Ítem {seleccion} en todos los sujetos analizados.")

    # --- TABLA E INFO ---
    with st.expander("🔍 Ver Matriz de Datos Final"):
        st.dataframe(df_analisis, hide_index=True)

else:
    st.warning("⚠️ Esperando archivo CSV.")