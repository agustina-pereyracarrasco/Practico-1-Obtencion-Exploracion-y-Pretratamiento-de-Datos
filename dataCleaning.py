import pandas as pd
print("Pandas cargado correctamente")
print("Versión:", pd.__version__)

df = pd.read_csv("Tema_17.csv")
print(df.head())
