import csv
import pandas as pd

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
INPUT_TXT =     "./Data/Vehiculos/PARQUE-VEHICULAR-2007-2025-FULL.txt"
OUTPUT_CSV =    "./Data/Vehiculos/PARQUE-VEHICULAR-2007-2025-FULL.csv"

ENCODING_INPUT = "cp1252"
ENCODING_OUTPUT = "utf-8"

# ============================================================================
# PASO 1: LEER TXT (PIPE-DELIMITED)
# ============================================================================
print("=" * 80)
print("PASO 1: Leyendo archivo txt...")
print("=" * 80)

rows = []
with open(INPUT_TXT, "r", encoding=ENCODING_INPUT, newline="") as infile:
    reader = csv.reader(
        infile,
        delimiter="|",
        quotechar='"',
        escapechar="\\"
    )
    for row in reader:
        rows.append(row)

if not rows:
    raise ValueError("El archivo de entrada está vacío.")

# ============================================================================
# PASO 2: VALIDAR ESTRUCTURA DEL CSV
# ============================================================================
print("\n" + "=" * 80)
print("PASO 2: Validando estructura del CSV...")
print("=" * 80)

header = rows[0]
expected_columns = len(header)

print(f"\nColumnas esperadas: {expected_columns}")

errores_encontrados = False
filas_validas = [header]
for line_number, row in enumerate(rows[1:], start=2):
    current_columns = len(row)
    if current_columns != expected_columns:
        if not errores_encontrados:
            print("\nFILAS CON PROBLEMAS DETECTADAS:\n")
            errores_encontrados = True

        print("=" * 80)
        print(f"Fila: {line_number}")
        print(f"Esperadas: {expected_columns} | Encontradas: {current_columns}")
        print(f"Primeras columnas: {row[:5]}")
        print(f"Fila completa: {row}")
    else:
        filas_validas.append(row)

if not errores_encontrados:
    print("\n✓ Todas las filas tienen la estructura correcta")
else:
    filas_omitidas = len(rows) - len(filas_validas)
    print(f"\nSe omitirán {filas_omitidas} filas con estructura inválida")

# ============================================================================
# PASO 3: FILTRAR Y PROCESAR CON PANDAS
# ============================================================================
print("\n" + "=" * 80)
print("PASO 3: Aplicando filtros...")
print("=" * 80)

if len(filas_validas) <= 1:
    raise ValueError("No hay filas válidas para procesar después de la validación.")

df = pd.DataFrame(filas_validas[1:], columns=filas_validas[0])

# Limpieza de columnas
df.columns = df.columns.str.strip()
df["ANIO_ALZA"] = pd.to_numeric(df["ANIO_ALZA"], errors="coerce")

# Filtros principales
df_filtrado = df[
    (df["NOMBRE_DEPARTAMENTO"] == "GUATEMALA") &
    (df["NOMBRE_MUNICIPIO"] == "GUATEMALA") &
    (df["ANIO_ALZA"] < 2025)
    ]

print(f"\nRegistros después de filtros geográficos: {len(df_filtrado):,}")

# Mostrar tipos de vehículo únicos
tipo_vehiculo = sorted(df_filtrado["TIPO_VEHICULO"].dropna().unique())
print(f"\nTipos de vehículo encontrados: {len(tipo_vehiculo)}")
print("\nVALORES ÚNICOS TIPO_VEHICULO (FILTRADO):")
for tipo in tipo_vehiculo:
    print(f"{tipo}")

# Definir categoría de livianoss
livianos = {
    "AUTOMOVIL",
    "AMBULANCIA",
    "JEEP",
    "PICK UP",
    "CARRO PARA GOLF",
    "CAMIONETA",
    "CAMIONETA AGRICOLA",
    "CAMIONETA SPORT",
    "CAMIONETILLA",
    "PANEL",
    "MICROBUS",
    "MICROBUS ESCOLAR",
    "MINIBUS",
    "MOTO",
    "SCOOTER",
    "TRIMOTO",
    "CUATRIMOTO",
    "LIMOSINA",
    "CARRO FUNEBRE",
    "VEHICULO RUSTICO"
}

# Filtrar solo livianoss
df_livianos = df_filtrado[
    df_filtrado["TIPO_VEHICULO"].isin(livianos)
]
# df_livianos=df_filtrado

print(f"\nRegistros de vehículos livianos: {len(df_livianos):,}")

# ============================================================================
# GUARDAR RESULTADO FINAL
# ============================================================================
df_livianos.to_csv(
    OUTPUT_CSV,
    index=False,
    encoding=ENCODING_OUTPUT
)

print("\n" + "=" * 80)
print("✓ PROCESO COMPLETADO")
print(f"✓ Archivo final guardado: {OUTPUT_CSV}")
print("=" * 80)