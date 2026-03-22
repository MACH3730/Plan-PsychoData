import pandas as pd
import numpy as np

def es_dicotomico(df):
    # Ignorar la columna ID si está presente
    items = df.drop(columns=['ID']) if 'ID' in df.columns else df
    # Obtener valores únicos ignorando nulos
    valores = pd.unique(items.values.ravel())
    valores = [v for v in valores if pd.notna(v)]
    # Es dicotómico si el conjunto de valores es un subconjunto de {0, 1}
    return set(valores).issubset({0, 1})

def limpiar_datos(df, metodo="Eliminar sujeto"):
    df = df.replace(r'^\s*$', np.nan, regex=True)
    if metodo == "Eliminar sujeto":
        return df.dropna().reset_index(drop=True)
    return df.fillna(0)

def procesar_y_ordenar_items(df):
    id_col = df['ID'].reset_index(drop=True)
    items = df.drop(columns=['ID']).apply(pd.to_numeric).reset_index(drop=True)
    p = items.mean().sort_values()
    items_ordenados = items[p.index]
    return pd.concat([id_col, items_ordenados], axis=1)

def calcular_alfa_cronbach(df):
    items = df.drop(columns=['ID']).apply(pd.to_numeric)
    k = items.shape[1]
    sum_var_items = items.var(ddof=1).sum()
    var_total = items.sum(axis=1).var(ddof=1)
    if var_total == 0 or k <= 1: return 0
    return (k / (k - 1)) * (1 - (sum_var_items / var_total))

def calcular_fiabilidad_mitades(df, metodo='spearman_brown'):
    items = df.drop(columns=['ID']).apply(pd.to_numeric)
    m1 = items.iloc[:, 0::2].sum(axis=1)
    m2 = items.iloc[:, 1::2].sum(axis=1)
    if metodo == 'spearman_brown':
        r = np.corrcoef(m1, m2)[0, 1]
        return (2 * r) / (1 + r) if (1 + r) != 0 else 0
    elif metodo == 'rulon':
        var_diff = (m1 - m2).var(ddof=1)
        var_total = (m1 + m2).var(ddof=1)
        return 1 - (var_diff / var_total) if var_total != 0 else 0
    return 0