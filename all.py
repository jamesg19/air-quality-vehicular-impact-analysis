import csv
import pandas as pd

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
INPUT_TXT = "archivo.txt"
TEMP_CSV = "archivo.csv"
OUTPUT_CSV = "parque_vehicular_liviano.csv"

ENCODING_INPUT = "cp1252"
ENCODING_OUTPUT = "utf-8"

# ============================================================================
# PASO 1: CONVERTIR TXT (PIPE-DELIMITED) A CSV
# ============================================================================
print("=" * 80)
print("PASO 1: Convirtiendo archivo.txt a CSV...")
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

with open(TEMP_CSV, "w", encoding=ENCODING_OUTPUT, newline="") as outfile:
    writer = csv.writer(
        outfile,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
    )
    writer.writerows(rows)

print(f"✓ Archivo convertido: {TEMP_CSV}")

# ============================================================================
# PASO 2: VALIDAR ESTRUCTURA DEL CSV
# ============================================================================
print("\n" + "=" * 80)
print("PASO 2: Validando estructura del CSV...")
print("=" * 80)

with open(TEMP_CSV, "r", encoding=ENCODING_OUTPUT) as f:
    reader = csv.reader(f)
    header = next(reader)
    expected_columns = len(header)
    
    print(f"\nColumnas esperadas: {expected_columns}")
    
    errores_encontrados = False
    for line_number, row in enumerate(reader, start=2):
        current_columns = len(row)
        if current_columns != expected_columns:
            if not errores_encontrados:
                print("\n⚠ FILAS CON PROBLEMAS DETECTADAS:\n")
                errores_encontrados = True
            
            print("=" * 80)
            print(f"Fila: {line_number}")
            print(f"Esperadas: {expected_columns} | Encontradas: {current_columns}")
            print(f"Primeras columnas: {row[:5]}")
            print(f"Fila completa: {row}")
    
    if not errores_encontrados:
        print("\n✓ Todas las filas tienen la estructura correcta")

# ============================================================================
# PASO 3: FILTRAR Y PROCESAR CON PANDAS
# ============================================================================
print("\n" + "=" * 80)
print("PASO 3: Aplicando filtros...")
print("=" * 80)

df = pd.read_csv(
    TEMP_CSV,
    encoding=ENCODING_OUTPUT,
    sep=",",
    engine="python",
    on_bad_lines="skip"
)

# Limpieza de columnas
df.columns = df.columns.str.strip()

# Filtros principales
df_filtrado = df[
    (df["NOMBRE_DEPARTAMENTO"] == "GUATEMALA") &
    (df["NOMBRE_MUNICIPIO"] == "GUATEMALA") &
    (df["ANIO_ALZA"] != 2026)
]

print(f"\nRegistros después de filtros geográficos: {len(df_filtrado):,}")

# Mostrar tipos de vehículo únicos
tipo_vehiculo = sorted(df_filtrado["TIPO_VEHICULO"].dropna().unique())
print(f"\nTipos de vehículo encontrados: {len(tipo_vehiculo)}")
print("\nVALORES ÚNICOS TIPO_VEHICULO (FILTRADO):")
for tipo in tipo_vehiculo:
    print(f"  - {tipo}")

# Definir categoría de livianos
livianos = {
    "AUTOMOVIL",
    "JEEP",
    "PICK UP",
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

# Filtrar solo livianos
df_livianos = df_filtrado[
    df_filtrado["TIPO_VEHICULO"].isin(livianos)
]

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
print(f"✓ PROCESO COMPLETADO")
print(f"✓ Archivo final guardado: {OUTPUT_CSV}")
print("=" * 80)