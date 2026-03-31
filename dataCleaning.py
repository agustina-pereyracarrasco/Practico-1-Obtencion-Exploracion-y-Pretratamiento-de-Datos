#----- Uso de biblioteca pandas -----
from numpy import dtype
import pandas as pd
import matplotlib
import numpy as np
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

cols = ["CO(GT)", "NMHC(GT)", "C6H6(GT)", "NOx(GT)", "NO2(GT)", "PT08.S5(O3)"]
df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
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


#-----Check inconsistencia en los datos
print("INICIO CHECK INCONSISTENCIA")


#Temperatura

temperaturas_inconsistentes = (df["T"] < -50) | (df["T"] > 60) #rangos imposibles
print("Cantidad de filas con temperaturas no relevantes: ", temperaturas_inconsistentes.sum())
df.loc[temperaturas_inconsistentes, "T"] = np.nan #reemplazar inconsistencias por NaN para tratar mas tarde
#print("NaN en T:", df["T"].isna().sum()) #check Nan


#Humedad

rh_inconsistente = (df["RH"] < 0) | (df["RH"] > 100)
print("Filas con inconsistencias RH: ", rh_inconsistente.sum())

ah_inconsistente = df["AH"] < 0
print("Filas con inconsistencias AH: ", ah_inconsistente.sum())


#Gases

cols = ["CO(GT)", "NMHC(GT)", "C6H6(GT)", "NOx(GT)", "NO2(GT)", "PT08.S5(O3)"]

df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")


for col in cols:
    print(col, (df[col] < 0).sum()) #Valores negativos
    print(df[col].describe()) #muestra estadisticas generales de cada columna (cantidad de filas, min, max, promedio..)
    


df[cols].isna().sum() #Valores faltantes

conteo = (df['PT08.S5(O3)'] > 1374).sum()
print("Valores limites de ozono: ", conteo)
correctos = df['PT08.S5(O3)'].count()
print("Valores no nulos de ozono: ",correctos)
 
df[cols].apply(pd.to_numeric, errors="coerce").hist(bins=30)
plt.show()

df.boxplot(column=cols)
plt.xticks(rotation=45)
plt.show()

df.groupby("Time_num")["CO(GT)"].mean().plot(kind="bar")

plt.xlabel("Hora del día")
plt.ylabel("CO promedio")
plt.title("Concentración promedio de CO por hora")

plt.xticks(rotation=0)  # opcional
plt.show()





