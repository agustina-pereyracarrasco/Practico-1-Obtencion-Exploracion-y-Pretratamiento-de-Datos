#----- Uso de biblioteca pandas -----
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")  # o Qt5Agg

import matplotlib.pyplot as plt

#----- 1) Carga de datos -----

df = pd.read_csv("Tema_17.csv")

#-------------- ANÁLISIS EXPLORATORIO --------------
# ----- a) Calcular y mostrar la cantidad de filas y columnas -----

cantFilas, cantColumnas = df.shape
print(f"Cantidad de filas: {cantFilas}, Cantidad de columnas: {cantColumnas}")

#----- b) Observar y mostrar las primeras 5 filas -----

print(f"Primeras 5 filas: {df.head()}")

#----- c) Evaluar la existencia de datos faltantes y duplicados. Cuantificarlos y calcular el porcentaje sobre el total de filas.-----

#Datos faltantes


df = df.replace(-200, pd.NA) #identificar todos los valores faltantes

faltantes = df.isnull().sum().sum()
print(f"Cantidad de datos faltantes: {faltantes}")
cantidadCeldas= df.shape[0]*df.shape[1]
print(f"Porcentaje de datos faltantes sobre el total: {round((faltantes/cantidadCeldas)*100,2)}%")

#Datos duplicados
duplicados = df.duplicated().sum()
print(f"Cantidad de datos duplicados sobre el total: {duplicados}")
print(f"Porcentaje de datos duplicados sobre el total: {round((duplicados/cantFilas)*100,2)}%")

#----- d) Para los datos faltantes, evaluar posibles motivos de esto en cada caso.-----

df["Datetime"] = pd.to_datetime(
    df["Date"] + " " + df["Time"],
    format="%d/%m/%Y %H.%M.%S",
    errors="coerce"
)

df = df.dropna(subset=["Datetime"])
df = df.set_index("Datetime").sort_index()

#----- Para variables discretas, evaluar los posibles valores de cada variable (valores únicos).-----

valores_unicos = df.index.unique()
print(valores_unicos)

df = df.reset_index()
df["CO(GT)"].hist(bins=30)

plt.title("Distribución de CO(GT)")
plt.xlabel("CO(GT)")
plt.ylabel("Frecuencia")

plt.show()

#----- Cuantificar los valores únicos del punto e) y realizar histogramas.-----
#----- Evaluar la existencia de datos inconsistentes ------


