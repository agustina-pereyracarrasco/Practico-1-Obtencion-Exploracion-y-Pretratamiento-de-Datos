#----- Uso de biblioteca pandas -----
from numpy import dtype
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

#print(df.dtypes)

#Calculo de datos faltantes
faltantes = df.isnull().sum().sum()
print(f"Cantidad de datos faltantes: {faltantes}")
cantidadCeldas= df.shape[0]*df.shape[1]
print(f"Porcentaje de datos faltantes sobre el total: {round((faltantes/cantidadCeldas)*100,2)}%")

#Calculo de datos duplicados
duplicados = df.duplicated().sum()
print(f"Cantidad de datos duplicados sobre el total: {duplicados}")
print(f"Porcentaje de datos duplicados sobre el total: {round((duplicados/cantFilas)*100,2)}%")

#----- d) Para los datos faltantes, evaluar posibles motivos de esto en cada caso.-----
#Teórico


#----- Para variables discretas, evaluar los posibles valores de cada variable (valores únicos).-----
#Teórico



#----- Cuantificar los valores únicos del punto e) y realizar histogramas.-----
df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y", errors="coerce")
df['Time'] = pd.to_datetime(df['Time'], format="%H.%M.%S", errors="coerce").dt.time



print(df.dtypes)



print(df.head(100))
print(df['Date'].nunique())
print(df["Time"].nunique())

print(df.dtypes)


df["Time_num"] = df["Time"].apply(lambda x: x.hour if pd.notna(x) else None)

df["Time_num"].value_counts().sort_index().plot(kind="bar")

plt.xlabel("Hora")
plt.ylabel("Frecuencia")
plt.title("Cantidad de registros por hora")
plt.xticks(rotation=45)
plt.show()


#df["CO(GT)"] = pd.to_numeric(df["CO(GT)"], errors="coerce")
#df.groupby("Time_num")["CO(GT)"].mean().plot()

#plt.xlabel("Hora")
#plt.ylabel("Promedio de CO")
#plt.title("Valores de CO promedio por hora")

#plt.show()



#df.groupby("Time_num")["NMHC(GT)"].mean().plot()

#lt.xlabel("Hora")
#plt.ylabel("Promedio de NMHC")
#plt.title("Valores de NMHC promedio por hora")

#plt.show()

#----- Evaluar la existencia de datos inconsistentes ------


