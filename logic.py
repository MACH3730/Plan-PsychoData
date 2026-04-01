import pandas as pd
import numpy as np

def procesar_psicometria(df, metodo, nulos_opcion):
    # 1. GESTIÓN DE NULOS
    # Convertimos a numérico y gestionamos nulos (importante para el CSV del Word)
    id_col = df.columns[0]
    items_only = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
    
    if nulos_opcion == "Eliminar sujeto":
        items_df = items_only.dropna().copy()
        df = df.loc[items_df.index] # Sincronizar IDs
    else:
        items_df = items_only.fillna(0).copy()

    # 2. ALFA DE CRONBACH (Cuasivarianza ddof=1)
    n_items = items_df.shape[1]
    varianzas_items = items_df.var(ddof=1).sum()
    suma_total_test = items_df.sum(axis=1)
    varianza_total = suma_total_test.var(ddof=1)
    
    if varianza_total <= 0 or n_items <= 1:
        alfa = 0.0
    else:
        alfa = (n_items / (n_items - 1)) * (1 - (varianzas_items / varianza_total))

    # 3. MITADES (Pares vs Impares)
    mitad_1 = items_df.iloc[:, 0::2].sum(axis=1)
    mitad_2 = items_df.iloc[:, 1::2].sum(axis=1)
    
    # Seleccionamos la fórmula según la opción de la izquierda
    if metodo == "rulon":
        # Rulon: 1 - (Var_dif / Var_total)
        diferencias = mitad_1 - mitad_2
        fiabilidad_mitades = 1 - (diferencias.var(ddof=1) / varianza_total) if varianza_total != 0 else 0
    
    elif metodo == "guttman":
        # Guttman-Flanagan: 2 * (1 - (Var_m1 + Var_m2) / Var_total)
        var_m1 = mitad_1.var(ddof=1)
        var_m2 = mitad_2.var(ddof=1)
        fiabilidad_mitades = 2 * (1 - (var_m1 + var_m2) / varianza_total) if varianza_total != 0 else 0
    
    else: # spearman_brown por defecto
        r_12 = np.corrcoef(mitad_1, mitad_2)[0, 1]
        if np.isnan(r_12):
            fiabilidad_mitades = 0
        else:
            fiabilidad_mitades = (2 * r_12) / (1 + r_12)

    return {
        "alfa": f"{max(0, alfa):.4f}",
        "mitades": f"{max(0, fiabilidad_mitades):.4f}",
        "ids": df[id_col].astype(str).tolist(),
        "items": items_df.columns.tolist(),
        "matriz": items_df.to_dict(orient='list')
    }