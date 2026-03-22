# 🧠 Plan PsychoData: Psychometric Analysis Engine

**Plan PsychoData** es una herramienta de análisis estadístico diseñada para la evaluación de tests bajo el marco de la **Teoría Clásica de los Tests (TCT)**. La aplicación automatiza el proceso de limpieza de datos, ordenación de ítems y cálculo de fiabilidad, garantizando rigor metodológico en cada paso.

## 🚀 Características Principales

* **Detección Automática de Ítems:** Identifica si los datos son dicotómicos (0/1) o de escala (Likert), adaptando el nombre del coeficiente a **KR-20** o **Alfa de Cronbach** respectivamente.
* **Gestión de Nulos Inteligente:** Permite elegir entre la eliminación de sujetos (listwise deletion) o la sustitución por error (0), asegurando la integridad de la matriz de datos.
* **Ordenación por Dificultad ($p$):** Antes de cualquier cálculo, el motor reordena sistemáticamente los ítems según su índice de dificultad. Esto optimiza la creación de formas paralelas y estabiliza los coeficientes de mitades.
* **Análisis Visual Dinámico:** * **Trayectoria de Sujetos:** Visualización individual del patrón de respuesta de un sujeto a través de los ítems ordenados.
    * **Rendimiento de Ítems:** Gráficos de línea para analizar el comportamiento de una sola variable a través de toda la muestra.
* **Múltiples Métricas de Fiabilidad:**
    * **Alfa de Cronbach / KR-20:** Consistencia interna basada en la covarianza de los ítems.
    * **Spearman-Brown:** Estimación de fiabilidad por división de mitades.
    * **Rulon:** Método robusto basado en la varianza de las diferencias entre mitades.

## 🛠️ Tecnologías Utilizadas

* **Python 3.12+**
* **Streamlit:** Interfaz de usuario interactiva y web-based.
* **Pandas & NumPy:** Procesamiento de matrices y cálculo de cuasivarianzas de alta precisión.
* **UV:** Gestor de paquetes de última generación.

## 📋 Estructura del CSV de Entrada

Para un correcto funcionamiento, el archivo CSV debe cumplir con:
1.  Una columna obligatoria llamada **`ID`**.
2.  Columnas de ítems con encabezados únicos (ej. `V1, V2, V3...`).
3.  Valores numéricos. Los espacios vacíos se gestionan según la configuración de la app.

## 💻 Instalación y Uso

1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/MACH3730/Plan-PsychoData.git](https://github.com/MACH3730/Plan-PsychoData.git)
    ```
2.  Ejecuta la aplicación con `uv`:
    ```bash
    uv run streamlit run app.py
    ```

## ⚖️ Metodología y Rigor

El sistema está diseñado para evitar errores comunes en software genérico:
* **Cuasivariancia:** Se utiliza el denominador $n-1$ para obtener estimadores insesgados de la varianza muestral.
* **Optimización de Mitades:** La ordenación previa por dificultad ($p$) busca la convergencia entre Spearman-Brown y Rulon, indicando una división en mitades máxima y paralela.

---
*Desarrollado como herramienta de soporte para profesionales de la Psicometría y las Ciencias del Comportamiento.*

### 📩 Contacto
Si tienes alguna duda sobre el proyecto o estás interesado en colaborar, ¡no dudes en contactarme!

**Email:** [marcosrock.dev@proton.me](mailto:marcosrock.dev@proton.me)