import pandas as pd

# Leer el Excel
df = pd.read_excel("ventas_globales_2024_2026.xlsx")

# Ver dimensiones
print("=" * 60)
print(f"DIMENSIONES: {df.shape[0]} filas x {df.shape[1]} columnas")
print("=" * 60)

# Ver columnas y tipos
print("\n=== COLUMNAS Y TIPOS DE DATOS ===")
print(df.dtypes)

# Ver primeras 5 filas
print("\n=== PRIMERAS 5 FILAS ===")
print(df.head())

# Ver valores únicos por columna (para saber qué filtros podemos hacer)
print("\n=== VALORES ÚNICOS POR COLUMNA ===")
for col in df.columns:
    n_unicos = df[col].nunique()
    print(f"\n▶ {col} ({n_unicos} valores únicos):")
    if n_unicos <= 15:
        print(f"   {list(df[col].dropna().unique())}")
    else:
        print(f"   Ejemplos: {list(df[col].dropna().unique()[:5])} ...")

# Ver si hay valores nulos
print("\n=== VALORES NULOS POR COLUMNA ===")
print(df.isnull().sum())