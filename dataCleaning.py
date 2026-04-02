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
df = df.replace("invalid_value", -200)
df = df.replace(-200, pd.NA) #identificar todos los valores faltantes

#Calculo de datos faltantes
faltantes = df.isnull().sum().sum()
print(f"Cantidad de datos faltantes: {faltantes}")
cantidadCeldas= df.shape[0]*df.shape[1]
print(f"Porcentaje de datos faltantes sobre el total: {round((faltantes/cantidadCeldas)*100,2)}%")

#Calculo de datos duplicados
duplicados = df.duplicated().sum()
print(f"Cantidad de datos duplicados sobre el total: {duplicados}")
print(f"Porcentaje de datos duplicados sobre el total: {round((duplicados/cantFilas)*100,2)}%")

#----- Cuantificar los valores únicos del punto e) y realizar histogramas.-----#

df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y", errors="coerce")
df['Time'] = pd.to_datetime(df['Time'], format="%H.%M.%S", errors="coerce").dt.time

print(df.dtypes)

print(df.head(100))
print(df['Date'].nunique())
print(df["Time"].nunique())

print(df.dtypes)

df["Time_num"] = df["Time"].apply(lambda x: x.hour if pd.notna(x) else None) #nueva columna con las horas representadas de 0 a 23

#Grafica registros por hora
df["Time_num"].value_counts().sort_index().plot(kind="bar")
plt.xlabel("Hora del día (0–23)")
plt.ylabel("Cantidad de registros")
plt.title("Distribución de mediciones a lo largo del día")
plt.xticks(rotation=0)
plt.grid(axis="y")

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

#Valores limites

co_inconsistente = (df["CO(GT)"] < 0) | (df["CO(GT)"] > 80)    
print("Valores limites de CO: ",co_inconsistente.sum())

nmhc_inconsistente = ((df['NMHC(GT)'] > 1000)|((df['NMHC(GT)']) < 0)).sum()
print("Valores limites de NMHC", nmhc_inconsistente)

#print(df["NMHC(GT)"].isna().mean()) usar en limpieza (muchos valores NaN)

c6h6_inconsistente = ((df['C6H6(GT)'] > 200)|(df['C6H6(GT)'] < 0)).sum()
print("Valores limites de C6H6", c6h6_inconsistente)

nox_inconsistente = (df["NOx(GT)"] < 0) | (df["NOx(GT)"] > 1000)
print("Valores limites nox: ",nox_inconsistente.sum())

no2_inconsistente = (df["NO2(GT)"] < 0) | (df["NO2(GT)"] > 500)
print("Valores limites no2: ",no2_inconsistente.sum())

df[cols].isna().sum() #Valores faltantes

conteoOzono = (df['PT08.S5(O3)'] > 1374).sum()
print("Valores limites de ozono: ", conteoOzono)
correctos = df['PT08.S5(O3)'].count()
print("Valores no nulos de ozono: ",correctos)


#Graficas


df[cols].apply(pd.to_numeric, errors="coerce").hist(bins=30, figsize=(12,8))
plt.suptitle("Distribución de contaminantes", fontsize=16)
plt.show()


plt.figure(figsize=(12,6))
df.boxplot(column=cols)
plt.title("Detección de outliers en contaminantes")
plt.xlabel("Contaminantes")
plt.ylabel("Concentración")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


for col in cols:
    plt.figure()
    
    df.groupby("Time_num")[col].mean().plot(kind="bar")
    
    plt.xlabel("Hora del día (0–23)")
    plt.ylabel(f"Concentración promedio de {col}")
    plt.title(f"Variación diaria de {col}")
    
    plt.xticks(rotation=0)
    plt.grid(axis="y")
    
    plt.show()





