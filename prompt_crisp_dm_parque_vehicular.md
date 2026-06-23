Actúa como un Científico de Datos Experto y Asesor de Tesis de Maestría en Ciencia de Datos. Tu objetivo es generar un Jupyter Notebook completo y detallado en Python titulado "05_liviano_pm25.ipynb". Este notebook forma parte de una investigación de maestría titulada: "ANÁLISIS DEL EFECTO DEL AUMENTO DEL PARQUE VEHICULAR LIVIANO Y EL DETERIORO DE LA CALIDAD DEL AIRE CON PM2.5 EN LA CIUDAD CAPITAL, GUATEMALA 2022-2025".

El desarrollo debe seguir estrictamente la metodología CRISP-DM y estructurarse en celdas de Markdown explicativas y bloques de código de Python limpios, funcionales y completamente escritos (evita usar comentarios de marcador de posición como "# Tu código aquí").

---

### INFORMACIÓN DE LOS DATASETS DISPONIBLES:

1. `PARQUE-VEHICULAR-LIVIANO-2007-2025-FULL.csv` (Periodicidad mensual, datos de 2007 a 2025)
   - Columnas principales: 'ANIO_ALZA', 'MES', 'MODELO_VEHICULO', 'LINEA_VEHICULO', 'TIPO_VEHICULO', 'USO_VEHICULO', 'MARCA_VEHICULO', 'CANTIDAD'.
   - NOTA CRÍTICA: La columna 'CANTIDAD' contiene el número de vehículos agrupados. No debes contar filas, debes aplicar un `.sum()` sobre esta columna al agrupar. 'ANIO_ALZA' y 'MES' determinan la fecha de ingreso (Alta) a la circulación. 'MODELO_VEHICULO' es el año de fabricación del vehículo.

2. `PM25_DAIRY_FULL_2022_2025.csv` (Periodicidad diaria, desde Marzo 2022 hasta Diciembre 2025)
   - Columnas: 'YEAR', 'MONTH', 'DAY', 'PM25'.
   - Unidades: μg/m³. 
   - NOTA CRÍTICA: Para hacer el análisis de series temporales y correlaciones, debes sincronizar la periodicidad reduciendo el dataset de PM2.5 a una media mensual (.mean()) agrupando por YEAR y MONTH, intersectando estrictamente el periodo común: Marzo 2022 a Diciembre 2025.

---

### REQUISITOS DEL DESARROLLO DEL NOTEBOOK (CRISP-DM):

Por favor, escribe el código completo y las explicaciones teóricas/académicas para cada fase:

#### FASE 1: Entendimiento del Negocio / Investigación
- Introducción corta en Markdown que ligue los objetivos de la tesis con los datos: el impacto de la emisión de vehículos livianos sobre las partículas finas PM2.5 en la Ciudad de Guatemala.

#### FASE 2: Entendimiento de los Datos
- Carga de librerías (`pandas`, `numpy`, `statsmodels`, `matplotlib`, `seaborn`, `scipy.stats`).
- Carga de los archivos CSV y análisis exploratorio inicial (tipos de datos, dimensiones, valores nulos y estadísticas descriptivas).

#### FASE 3: Preparación de los Datos
- **PM2.5:** Crear una columna datetime, filtrar desde marzo 2022 a diciembre 2025, y remuestrear/agrupar para obtener la **Media Mensual**.
- **Parque Vehicular (Altas):** Filtrar registros donde 'ANIO_ALZA' y 'MES' estén entre Marzo 2022 y Diciembre 2025. Agrupar sumando 'CANTIDAD'.
- **Parque Vehicular (Acumulado):** Calcular el inventario acumulado total circulante mes a mes dentro del periodo de estudio.
- **Merge:** Combinar los datasets en un único dataframe indexado por tiempo (mensual, `YYYY-MM`) para los análisis posteriores.

#### FASE 4: Modelado de Series Temporales (Dos Enfoques)
1. **Primera Forma - Modelo ARIMA:** - Realizar pruebas de estacionariedad (ADF Test) sobre la serie de PM2.5.
   - Ajustar un modelo ARIMA univariante para PM2.5 para establecer una línea base de predicción/comportamiento temporal intrínseco. Mostrar gráficos ACF y PACF.
2. **Segunda Forma - Modelo SARIMAX:**
   - Incorporar el componente estacional si aplica y, de manera crucial, incluir el volumen de parque vehicular liviano (Altas o Acumulado) como **variable exógena (`exog`)** para evaluar si el aumento vehicular explica directamente las variaciones del PM2.5.

#### FASE 5: Evaluación
- Comparar ambos modelos utilizando criterios estadísticos rigurosos: AIC, BIC, RMSE y MAE.
- Realizar un análisis de residuos (Prueba de Ljung-Box y normalidad) para validar los supuestos de los modelos de series de tiempo.

#### FASE 6: Apartados Extras - Análisis de Correlación Avanzado
Implementa celdas específicas de código y visualizaciones para responder detalladamente a las siguientes hipótesis de correlación (utiliza correlaciones de Pearson/Spearman y matrices/gráficos de dispersión según corresponda):

**1. Correlación con el ACUMULADO del parque vehicular (2022-2025) vs. PM2.5 Media Mensual:**
   - **1.1 Por 'MODELO_VEHICULO':** Agrupar el acumulado por el año de fabricación de los vehículos circulantes para ver si los modelos antiguos o recientes tienen mayor correlación con el deterioro del aire.
   - **1.2 Por 'TIPO_VEHICULO':** Evaluar la correlación segmentando el acumulado por categorías (Automóvil, Moto, Pick-up, etc.) contra el PM2.5 mensual.
   - **1.3 Por 'LINEA_VEHICULO':** Identificar cuáles son las líneas/modelos comerciales específicos más abundantes en el acumulado y analizar su correlación con los niveles de contaminación.

**2. Correlación utilizando SOLO LAS ALTAS del parque vehicular (Ingresos de Marzo 2022 a Diciembre 2025) vs. PM2.5 Media Mensual:**
   - **2.1 Por 'MODELO_VEHICULO':** Analizar la correlación entre el volumen de nuevos vehículos inscritos según su año de fabricación y las fluctuaciones del PM2.5.
   - **2.2 Por 'TIPO_VEHICULO':** Determinar qué tipo de vehículo nuevo que ingresa al parque vehicular (ej. el auge de las motocicletas o camionetas) muestra una correlación más fuerte con el PM2.5 del mes.
   - **2.3 Por 'LINEA_VEHICULO':** Analizar el impacto indexado por las líneas de vehículos específicos que ingresan mes a mes.

Genera el código completo de Python de extremo a extremo, asegurando que las visualizaciones usen matplotlib/seaborn con títulos claros y etiquetas en los ejes, adecuado para la presentación de resultados en una tesis de maestría.