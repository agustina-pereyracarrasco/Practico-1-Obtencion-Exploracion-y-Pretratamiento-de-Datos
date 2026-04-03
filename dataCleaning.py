#----- Uso de biblioteca pandas -----
from numpy import dtype
import pandas as pd
import matplotlib
import numpy as np
matplotlib.use("TkAgg")  # o Qt5Agg

import matplotlib.pyplot as plt

#----- 1) Carga de datos -----

def cargar_datos(ruta_archivo):
    df = pd.read_csv(ruta_archivo)
    return df

#-------------- ANÁLISIS EXPLORATORIO --------------
# ----- a) Calcular y mostrar la cantidad de filas y columnas -----
def analisis_exploratorio(df):
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
    faltantes = df.isnull().sum().sum() # suma de todos los datos faltantes por columna
    print(f"Cantidad de datos faltantes: {faltantes}")
    cantidadCeldas= df.shape[0]*df.shape[1] # calculo de cantidad total de celdas

    print(f"Porcentaje de datos faltantes sobre el total: {round((faltantes/cantidadCeldas)*100,2)}%")

     # Calculo de datos faltantes por columna
    for col in df.columns:
        faltantes_col = df[col].isnull().sum()

        # porcentaje dentro de la columna
        porcentaje_col = (faltantes_col / len(df)) * 100

        # porcentaje respecto a TODO el dataset
        porcentaje_total = (faltantes_col / cantidadCeldas) * 100

        print(
            f"Columna: {col} | Faltantes: {faltantes_col} | "
            f"% Columna: {porcentaje_col:.2f}% | % Total dataset: {porcentaje_total:.2f}%"
        )


    #Calculo de datos duplicados
    duplicados = df.duplicated().sum() # suma de todas las filas duplicadas
    print(f"Cantidad de datos duplicados sobre el total: {duplicados}")
    print(f"Porcentaje de datos duplicados sobre el total: {round((duplicados/cantFilas)*100,2)}%") 

    #----- Cuantificar los valores únicos del punto e) y realizar histogramas.-----#

    #Gráfica

    df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y", errors="coerce")
    df['Time'] = pd.to_datetime(df['Time'], format="%H.%M.%S", errors="coerce").dt.time


    print(f"Valores unicos de fecha: ", df['Date'].nunique())
    print(f"Valores unicos de hora: ",df["Time"].nunique())


    df["Time_num"] = df["Time"].apply(lambda x: x.hour if pd.notna(x) else None) #nueva columna con las horas representadas de 0 a 23

    #Grafica registros por hora
    df["Time_num"].value_counts().sort_index().plot(kind="bar")
    plt.xlabel("Hora del día (0–23)")
    plt.ylabel("Cantidad de registros")
    plt.title("Distribución de mediciones a lo largo del día")
    plt.xticks(rotation=0)
    plt.grid(axis="y")

    plt.show()

    #Histograma

    # Date
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")

    # Time corregido: normaliza 18.00.00 -> 18:00:00 y luego convierte a datetime
    df["Time"] = pd.to_datetime(
        df["Time"].astype(str).str.replace(".", ":", regex=False),
        format="%H:%M:%S",
        errors="coerce"
    )

    print(df.dtypes)

    print(df.head(100))
    print(df["Date"].nunique())
    print(df["Time"].nunique())

    print(df.dtypes)

    # nueva columna con las horas representadas de 0 a 23
    df["Time_num"] = df["Time"].dt.hour

    # Histograma de mediciones por hora
    df["Time_num"].hist(bins=24)

    plt.xlabel("Hora del día (0–23)")
    plt.ylabel("Frecuencia")
    plt.title("Histograma de mediciones por hora")
    plt.xticks(range(24))
    plt.grid(axis="y")

    plt.show()


    #-----Check inconsistencia en los datos
    print("INICIO CHECK INCONSISTENCIA")

    # Date
    date_inconsistente = df["Date"].isna()  # Fechas inválidas o faltantes
    print("Filas con fechas inválidas o faltantes: ", date_inconsistente.sum())

    date_fuera_rango = (df["Date"] < "2004-03-10") | (df["Date"] > "2005-04-04")  # Fechas fuera de rango esperado
    print("Filas con fechas fuera de rango: ", date_fuera_rango.sum())

    # Time
    time_inconsistente = df["Time"].isna()  # Horas inválidas o faltantes
    print("Filas con horas inválidas o faltantes: ", time_inconsistente.sum())

    time_fuera_rango = (df["Time_num"] < 0) | (df["Time_num"] > 23)  # Horas fuera de rango
    print("Filas con horas fuera de rango: ", time_fuera_rango.sum())

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
    countNMHC = (df['NMHC(GT)'].count())
    print("Valores no nulos de nmhc: ", countNMHC)
    nmhc_nulos = df["NMHC(GT)"].isna().sum()
    print("Valores nulos nmhc: ", nmhc_nulos)

    #print(df["NMHC(GT)"].isna().mean()) usar en limpieza (muchos valores NaN)

    c6h6_inconsistente = ((df['C6H6(GT)'] > 200)|(df['C6H6(GT)'] < 0)).sum()
    print("Valores limites de C6H6", c6h6_inconsistente)

    nox_inconsistente = (df["NOx(GT)"] < 0) | (df["NOx(GT)"] > 1000)
    print("Valores limites nox: ",nox_inconsistente.sum())

    no2_inconsistente = (df["NO2(GT)"] < 0) | (df["NO2(GT)"] > 500)
    print("Valores limites no2: ",no2_inconsistente.sum())

    conteoOzono = (df['PT08.S5(O3)'] > 1374).sum()
    print("Valores limites de ozono: ", conteoOzono)


    #Graficas


    df[cols].apply(pd.to_numeric, errors="coerce").hist(bins=30, figsize=(12,8))
    plt.suptitle("Distribución de contaminantes", fontsize=16)
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
    
    return df


#Limpieza de datos
def limpieza_de_datos(df):

    #Eliminar columna NMHC
    f = df.drop(columns=["NMHC(GT)"])

    #Crear columna datetime
    df["fecha"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str), errors="coerce")

    #Eliminar filas sin fecha válida
    df = df.dropna(subset=["fecha"])

    cols = ["CO(GT)", "C6H6(GT)", "NOx(GT)", "NO2(GT)", "PT08.S5(O3)", "T", "RH", "AH"]
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")

    #Eliminar duplicados
    df = df.groupby("fecha").mean(numeric_only=True).reset_index()

    #Ordenar y setear índice temporal
    df = df.sort_values("fecha")
    df = df.set_index("fecha")

    #Crear rango completo de horas (rellenar fechas faltantes)
    rango = pd.date_range(start=df.index.min(), end=df.index.max(), freq="h")
    df = df.reindex(rango)

    #Columnas a interpolar
    cols = ["CO(GT)", "C6H6(GT)", "NOx(GT)", "NO2(GT)", "PT08.S5(O3)", "T", "RH", "AH"]

    #Interpolación temporal
    df[cols] = df[cols].interpolate(method="time", limit=3)

    #Relleno por promedio por hora
    df["hora"] = df.index.hour
    for col in cols:
        df[col] = df[col].fillna(df.groupby("hora")[col].transform("mean"))


    #Chequeo final
    print("NaN restantes por columna:")
    print(df[cols].isna().sum())


    #Limpieza de outliers con IQR

    for col in cols:  # Recorre cada columna (cada variable de contaminantes)

        Q1 = df[col].quantile(0.25)  
        #Calcula el primer cuartil (25%)
        #Es el valor por debajo del cual está el 25% de los datos

        Q3 = df[col].quantile(0.75)  
        #Calcula el tercer cuartil (75%)
        #Es el valor por debajo del cual está el 75% de los datos

        IQR = Q3 - Q1  
        #Calcula el rango intercuartílico (IQR)
        #Representa la dispersión del 50% central de los datos

        lower = Q1 - 1.5 * IQR  
        #Define el límite inferior
        #Valores menores a esto se consideran outliers

        upper = Q3 + 1.5 * IQR  
        #Define el límite superior
        #Valores mayores a esto se consideran outliers

        df[col] = df[col].clip(lower, upper)  
        #Recorta los valores extremos:
        #Si un valor es menor que lower, lo reemplaza por lower
        #Si un valor es mayor que upper, lo reemplaza por upper
        #Si está dentro del rango, lo deja igual


    #Normalización

    columnas_numericas = ["CO(GT)", "C6H6(GT)", "NOx(GT)", "NO2(GT)", "PT08.S5(O3)", "T", "RH", "AH"]

    for col in columnas_numericas:
        if col in df.columns:
            min_val = df[col].min()
            max_val = df[col].max()

            # Evitar división por cero
            if max_val != min_val:
                df[col] = (df[col] - min_val) / (max_val - min_val)
                print(f"{col} normalizada")
            else:
                print(f"{col} no se pudo normalizar (valores constantes)")



    df[cols].apply(pd.to_numeric, errors="coerce").hist(bins=30, figsize=(12,8))
    plt.suptitle("Distribución de contaminantes", fontsize=16)
    plt.show()


    df["Time_num"] = df.index.hour
    for col in cols:
        plt.figure()
    
        df.groupby("Time_num")[col].mean().plot(kind="bar")
    
        plt.xlabel("Hora del día (0–23)")
        plt.ylabel(f"Concentración promedio de {col}")
        plt.title(f"Variación diaria de {col}")
    
        plt.xticks(rotation=0)
        plt.grid(axis="y")
    
        plt.show()



if __name__=="__main__":
    
    df = analisis_exploratorio(cargar_datos("Tema_17.csv"))

    df_limpio = limpieza_de_datos(df)

