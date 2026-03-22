import streamlit as st
import pandas as pd
import numpy as np
from logic import (
    limpiar_datos, 
    es_dicotomico, 
    procesar_y_ordenar_items, 
    calcular_alfa_cronbach, 
    calcular_fiabilidad_mitades
)

# Configuración de la interfaz
st.set_page_config(page_title="PsychoData Engine v2", layout="wide")
st.title("🧠 Plan PsychoData: Análisis Psicométrico Profesional")
st.markdown("---")

# Panel de control lateral
with st.sidebar:
    st.header("⚙️ Configuración")
    uploaded_file = st.file_uploader("Carga tu archivo CSV", type="csv")
    
    st.subheader("Parámetros de Análisis")
    metodo_mitades = st.radio("Fórmula de Dos Mitades:", ["spearman_brown", "rulon"])
    opcion_nulos = st.radio("Gestión de nulos:", ["Eliminar sujeto", "Sustituir por 0"])
    
    st.divider()
    st.caption("Desarrollado para análisis de TCT (Teoría Clásica de los Tests).")

# Flujo principal de la aplicación
if uploaded_file:
    # 1. Lectura inicial
    df_raw = pd.read_csv(uploaded_file)
    
    # 2. Limpieza de datos (Detección de NaN y aplicación de estrategia)
    df_clean = limpiar_datos(df_raw, metodo=opcion_nulos)
    
    # 3. Ordenación Metodológica (Vital para que las mitades sean paralelas)
    df_analisis = procesar_y_ordenar_items(df_clean)
    
    # 4. Identificación del tipo de ítem
    # Usamos df_analisis sin la columna ID para verificar si es binario
    es_dicto = es_dicotomico(df_analisis)
    nombre_coeficiente = "Coeficiente KR-20" if es_dicto else "Alfa de Cronbach"
    
    # Resumen de la muestra
    st.info(f"📊 **Resumen del proceso:** {len(df_analisis)} sujetos analizados. Ítems ordenados por índice de dificultad (p).")

    # 5. Bloque de visualización de resultados
    col1, col2 = st.columns(2)
    
    with col1:
        val_alfa = calcular_alfa_cronbach(df_analisis)
        # Mostramos con 4 decimales para precisión psicométrica
        st.metric(label=nombre_coeficiente, value=f"{val_alfa:.4f}")
        st.caption("Consistencia interna (basada en la covarianza de los ítems).")

    with col2:
        val_mitades = calcular_fiabilidad_mitades(df_analisis, metodo=metodo_mitades.lower())
        st.metric(label=f"Fiabilidad {metodo_mitades.upper()}", value=f"{val_mitades:.4f}")
        st.caption(f"Cálculo por división de mitades ({metodo_mitades}).")

    # 6. Tabla de inspección
    st.markdown("### Matriz de Datos Final")
    st.write("Las columnas aparecen ordenadas de mayor a menor dificultad (basado en la media).")
    st.dataframe(df_analisis, hide_index=True)

    # Verificación de varianzas para Rulon si hay dudas
    if metodo_mitades == "rulon":
        with st.expander("Ver detalles técnicos de Rulon"):
            items_only = df_analisis.drop(columns=['ID'])
            m1 = items_only.iloc[:, 0::2].sum(axis=1)
            m2 = items_only.iloc[:, 1::2].sum(axis=1)
            st.write(f"Varianza de las diferencias (σ²d): { (m1-m2).var(ddof=1):.4f}")
            st.write(f"Varianza total (σ²t): { (m1+m2).var(ddof=1):.4f}")

else:
    st.warning("⚠️ Esperando la carga de un archivo CSV para iniciar los cálculos.")
    st.markdown("""
    **Instrucciones para el CSV:**
    1. Debe contener una columna llamada **ID**.
    2. El resto de columnas deben ser los ítems (V1, V2...).
    3. Los valores deben ser numéricos (0/1 para dicotómicos, escala para Likert).
    """)