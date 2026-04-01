import pandas as pd
import numpy as np

def procesar_psicometria(df, metodo, nulos_opcion):
    # 1. GESTIÓN DE DATOS Y NULOS
    id_col = df.columns[0]
    items_only = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
    
    if nulos_opcion == "Eliminar sujeto":
        items_df = items_only.dropna().copy()
        df = df.loc[items_df.index]
    else:
        items_df = items_only.fillna(0).copy()

    # 2. CÁLCULO DE MEDIAS Y ORDENACIÓN (Pág. 21 del formulario)
    # Calculamos la media de cada ítem para determinar su dificultad
    medias = items_df.mean().sort_values(ascending=False)
    
    # Reordenamos las columnas del DataFrame de mayor a menor media
    # Esto asegura que al dividir 0::2 y 1::2, las mitades estén equilibradas
    items_ordenados = items_df[medias.index]

    # 3. ALFA DE CRONBACH (Cuasivarianza ddof=1)
    n_items = items_ordenados.shape[1]
    varianzas_items = items_ordenados.var(ddof=1).sum()
    suma_total_test = items_ordenados.sum(axis=1)
    varianza_total = suma_total_test.var(ddof=1)
    
    if varianza_total <= 0 or n_items <= 1:
        alfa = 0.0
    else:
        alfa = (n_items / (n_items - 1)) * (1 - (varianzas_items / varianza_total))

    # 4. DIVISIÓN POR MITADES (Sobre los ítems ya ordenados por dificultad)
    # Mitad 1: Posiciones 0, 2, 4... (los más difíciles/fáciles de forma alternada)
    mitad_1 = items_ordenados.iloc[:, 0::2].sum(axis=1)
    # Mitad 2: Posiciones 1, 3, 5...
    mitad_2 = items_ordenados.iloc[:, 1::2].sum(axis=1)
    
    # 5. CÁLCULO DE FIABILIDAD SEGÚN MÉTODO ELEGIDO
    if metodo == "rulon":
        diferencias = mitad_1 - mitad_2
        fiabilidad_mitades = 1 - (diferencias.var(ddof=1) / varianza_total) if varianza_total != 0 else 0
    
    elif metodo == "guttman":
        var_m1 = mitad_1.var(ddof=1)
        var_m2 = mitad_2.var(ddof=1)
        fiabilidad_mitades = 2 * (1 - (var_m1 + var_m2) / varianza_total) if varianza_total != 0 else 0
    
    else: # spearman_brown
        r_12 = np.corrcoef(mitad_1, mitad_2)[0, 1]
        fiabilidad_mitades = (2 * r_12) / (1 + r_12) if not np.isnan(r_12) else 0

    return {
        "alfa": f"{max(0, alfa):.4f}",
        "mitades": f"{max(0, fiabilidad_mitades):.4f}",
        "ids": df[id_col].astype(str).tolist(),
        "items": items_df.columns.tolist(), # Mantenemos orden original para el gráfico
        "matriz": items_df.to_dict(orient='list')
    }