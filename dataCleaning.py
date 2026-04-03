#----- Uso de biblioteca pandas -----
from numpy import dtype
import pandas as pd
import matplotlib
import numpy as np
matplotlib.use("TkAgg")  

import matplotlib.pyplot as plt

#----- 1) Carga de datos -----
def cargar_datos(ruta_archivo):
    df = pd.read_csv(ruta_archivo)
    return df

def analisis_exploratorio(df):
    #-------------- ANÁLISIS EXPLORATORIO --------------
    print("----- INICIO DE ANÁLISIS EXPLORATORIO -----")
    # ----- a) Calcular y mostrar la cantidad de filas y columnas -----

    cantFilas, cantColumnas = df.shape
    print(f"Cantidad de filas: {cantFilas}, Cantidad de columnas: {cantColumnas}")

    #----- b) Observar y mostrar las primeras 5 filas -----

    print(f"Primeras 5 filas: {df.head()}")

    #----- c) Evaluar la existencia de datos faltantes y duplicados. Cuantificarlos y calcular el porcentaje sobre el total de filas.-----

    # Datos faltantes
    cols = ["CO(GT)", "NMHC(GT)", "C6H6(GT)", "NOx(GT)", "NO2(GT)", "PT08.S5(O3)"]
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
    df = df.replace("invalid_value", -200)
    df = df.replace(-200, pd.NA)  # identificar todos los valores faltantes

    # Calculo de datos faltantes totales
    faltantes = df.isnull().sum().sum()  # suma de todos los datos faltantes por columna
    print(f"Cantidad de datos faltantes: {faltantes}")
    cantidadCeldas = df.shape[0] * df.shape[1]  # calculo de cantidad total de celdas
    print(f"Porcentaje de datos faltantes sobre el total: {round((faltantes/cantidadCeldas)*100, 2)}%")

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

    # Calculo de datos duplicados
    duplicados = df.duplicated().sum()  # suma de todas las filas duplicadas
    print(f"Cantidad de datos duplicados sobre el total: {duplicados}")
    print(f"Porcentaje de datos duplicados sobre el total: {round((duplicados/cantFilas)*100, 2)}%")

    #----- Cuantificar los valores únicos del punto e) y realizar histogramas.-----#

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

    #----- Check inconsistencia en los datos -----
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

    # Temperatura
    df["T"] = pd.to_numeric(df["T"], errors="coerce")
    temperaturas_inconsistentes = (df["T"] < -50) | (df["T"] > 60)  # rangos imposibles
    print("Cantidad de filas con temperaturas no relevantes: ", temperaturas_inconsistentes.sum())
    df.loc[temperaturas_inconsistentes, "T"] = np.nan  # reemplazar inconsistencias por NaN para tratar mas tarde

    # Humedad
    df["RH"] = pd.to_numeric(df["RH"], errors="coerce")
    df["AH"] = pd.to_numeric(df["AH"], errors="coerce")

    rh_inconsistente = (df["RH"] < 0) | (df["RH"] > 100)
    print("Filas con inconsistencias RH: ", rh_inconsistente.sum())

    ah_inconsistente = df["AH"] < 0
    print("Filas con inconsistencias AH: ", ah_inconsistente.sum())

    # Gases
    cols = ["CO(GT)", "NMHC(GT)", "C6H6(GT)", "NOx(GT)", "NO2(GT)", "PT08.S5(O3)"]
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")

    for col in cols:
        print(col, (df[col] < 0).sum())  # Valores negativos
        print(df[col].describe())  # muestra estadisticas generales de cada columna

    # Valores limites
    co_inconsistente = (df["CO(GT)"] < 0) | (df["CO(GT)"] > 80)
    print("Valores limites de CO: ", co_inconsistente.sum())

    nmhc_inconsistente = ((df["NMHC(GT)"] > 1000) | (df["NMHC(GT)"] < 0)).sum()
    print("Valores limites de NMHC", nmhc_inconsistente)

    c6h6_inconsistente = ((df["C6H6(GT)"] > 200) | (df["C6H6(GT)"] < 0)).sum()
    print("Valores limites de C6H6", c6h6_inconsistente)

    nox_inconsistente = (df["NOx(GT)"] < 0) | (df["NOx(GT)"] > 1000)
    print("Valores limites nox: ", nox_inconsistente.sum())

    no2_inconsistente = (df["NO2(GT)"] < 0) | (df["NO2(GT)"] > 500)
    print("Valores limites no2: ", no2_inconsistente.sum())

    df[cols].isna().sum()  # Valores faltantes

    conteoOzono = (df["PT08.S5(O3)"] > 1374).sum()
    print("Valores limites de ozono: ", conteoOzono)
    correctos = df["PT08.S5(O3)"].count()
    print("Valores no nulos de ozono: ", correctos)

    # Graficas
    df[cols].apply(pd.to_numeric, errors="coerce").hist(bins=30, figsize=(12, 8))
    plt.suptitle("Distribución de contaminantes", fontsize=16)
    plt.show()

    plt.figure(figsize=(12, 6))
    df.boxplot(column=cols)
    plt.title("Detección de outliers en contaminantes")
    plt.xlabel("Contaminantes")
    plt.ylabel("Concentración")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

    for col in cols:
        serie = df.groupby("Time_num")[col].mean().dropna()

        if not serie.empty:
            plt.figure()
            serie.plot(kind="bar")

            plt.xlabel("Hora del día (0–23)")
            plt.ylabel(f"Concentración promedio de {col}")
            plt.title(f"Variación diaria de {col}")

            plt.xticks(rotation=0)
            plt.grid(axis="y")

            plt.show()
        else:
            print(f"No hay datos válidos para graficar {col}")
    
    print("----- FIN ANÁLISIS EXPLORATORIO ----- ")

    return df
    

def limpieza_datos(df):
    print("----- INICIO LIMPIEZA DE DATOS ----- ")

    print("----- FIN LIMPIEZA DE DATOS ----- ")

    return df

def normalizacion_datos(df):
    print("----- INICIO NORMALIZACIÓN -----")

    columnas_numericas = [
        "CO(GT)", "PT08.S1(CO)", "C6H6(GT)", "PT08.S2(NMHC)",
        "NOx(GT)", "PT08.S3(NOx)", "NO2(GT)", "PT08.S4(NO2)",
        "PT08.S5(O3)", "T", "RH", "AH"
    ]

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

    print("----- FIN NORMALIZACIÓN ----- ")
    return df


def main():

    df = cargar_datos("Tema_17.csv")
    df = analisis_exploratorio(df)
    df = limpieza_datos(df)
    df = normalizacion_datos(df)

    print("Proceso completo finalizado.")


if __name__ == "__main__":
    main()

