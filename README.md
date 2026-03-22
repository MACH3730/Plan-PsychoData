# 🧠 Plan PsychoData: Psychometric Analysis Engine

**Plan PsychoData** es una herramienta de análisis estadístico diseñada para la evaluación de tests bajo el marco de la **Teoría Clásica de los Tests (TCT)**. La aplicación automatiza el proceso de limpieza de datos, ordenación de ítems y cálculo de fiabilidad, garantizando rigor metodológico en cada paso.

## 🚀 Características Principales

* **Detección Automática de Ítems:** Identifica si los datos son dicotómicos (0/1) o de escala (Likert), adaptando el nombre del coeficiente a **KR-20** o **Alfa de Cronbach** respectivamente.
* **Gestión de Nulos Inteligente:** Permite elegir entre la eliminación de sujetos (listwise deletion) o la sustitución por error (0), asegurando la integridad de la matriz de datos.
* **Ordenación por Dificultad ($p$):** Antes de cualquier cálculo de división por mitades, el motor reordena sistemáticamente los ítems según su índice de dificultad. Esto optimiza la creación de formas paralelas y estabiliza los coeficientes.
* **Múltiples Métricas de Fiabilidad:**
    * **Alfa de Cronbach / KR-20:** Medida de consistencia interna basada en la covarianza de los ítems.
    * **Spearman-Brown:** Estimación de la fiabilidad para el test completo tras la división en mitades.
    * **Rulon:** Método basado en la varianza de las diferencias entre mitades, más robusto ante la falta de equivalencia perfecta.

## 🛠️ Tecnologías Utilizadas

* **Python 3.12+**
* **Streamlit:** Para la interfaz de usuario interactiva.
* **Pandas & NumPy:** Para el procesamiento de matrices y cálculos estadísticos de alta precisión.
* **UV:** Gestor de paquetes ultrarrápido para la ejecución del entorno.

## 📋 Estructura del CSV de Entrada

Para un correcto funcionamiento, el archivo CSV debe cumplir con:
1.  Una columna obligatoria llamada **`ID`**.
2.  Columnas de ítems con encabezados únicos (ej. `V1, V2, V3...`).
3.  Valores numéricos. Los espacios vacíos serán gestionados según la opción de limpieza seleccionada en la app.

## 💻 Instalación y Uso

1.  Clona el repositorio o descarga los archivos.
2.  Asegúrate de tener instalada la biblioteca `uv`.
3.  Ejecuta la aplicación:
    ```bash
    uv run streamlit run app.py
    ```

## ⚖️ Metodología y Rigor

El sistema está diseñado para evitar los errores comunes en software estadístico genérico:
* **Evita sesgos de varianza:** Se utilizan grados de libertad corregidos ($n-1$) para el cálculo de varianzas muestrales.
* **Convergencia de Mitades:** Mediante la ordenación sistemática de ítems, se busca la convergencia de Spearman-Brown y Rulon, indicando una división en mitades óptima y paralela.

---
*Desarrollado como herramienta de soporte para profesionales de la Psicometría y las Ciencias del Comportamiento.*

📩 Contacto. Si tienes alguna duda sobre el proyecto o estás interesado en colaborar, ¡no dudes en contactarme!

Email: marcosrock.dev@proton.me