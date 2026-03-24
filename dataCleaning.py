import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.internals.managers import create_block_manager_from_column_arrays  

#-----------Carga de datos-----------#

df = pd.read_csv("Tema_17.csv")



#-----------Cantidad de filas y columnas-----------#

print(df.shape)



#-----------Imprimir primeras 5 filas-----------#

print(df.head()) 



#-----------Analisis exploratorio-----------#


print(df.dtypes)
