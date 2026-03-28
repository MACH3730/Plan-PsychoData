import pandas as pd
import numpy as np

def procesar_psicometria(df, metodo, nulos_opcion):
    # 1. GESTIÓN DE NULOS
    if nulos_opcion == "Eliminar sujeto":
        df = df.dropna().copy()
    else:
        df = df.fillna(0).copy()

    # Identificamos columna de ID (primera) e ítems (resto)
    id_col = df.columns[0]
    items_df = df.iloc[:, 1:]

    # 2. ALFA DE CRONBACH
    n_items = items_df.shape[1]
    varianzas_items = items_df.var(ddof=1).sum()
    varianza_total = items_df.sum(axis=1).var(ddof=1)
    
    if varianza_total == 0:
        alfa = 0.0
    else:
        alfa = (n_items / (n_items - 1)) * (1 - (varianzas_items / varianza_total))

    # 3. FIABILIDAD POR DOS MITADES (Pares vs Impares)
    mitad_1 = items_df.iloc[:, 0::2].sum(axis=1)
    mitad_2 = items_df.iloc[:, 1::2].sum(axis=1)
    
    r_12 = np.corrcoef(mitad_1, mitad_2)[0, 1]

    if metodo == "rulon":
        # Fórmula de Rulon: 1 - (Varianza de las diferencias / Varianza total)
        diferencias = mitad_1 - mitad_2
        fiabilidad_mitades = 1 - (diferencias.var(ddof=1) / items_df.sum(axis=1).var(ddof=1))
    else:
        # Spearman-Brown
        fiabilidad_mitades = (2 * r_12) / (1 + r_12)

    return {
        "alfa": f"{max(0, alfa):.4f}",
        "mitades": f"{max(0, fiabilidad_mitades):.4f}",
        "ids": df[id_col].astype(str).tolist(),
        "items": items_df.columns.tolist(),
        "matriz": items_df.to_dict(orient='list')
    }