import pandas as pd

#Funcion para buscar valores 
def buscar_valores(dataframe, lista_busqueda):
    resultados = []
    for valor in lista_busqueda:
        # Buscar si el valor está en cualquier parte de la columna 7
        mask = dataframe.iloc[:, 6].str.contains(valor, case=False, na=False)
        # Filtrar el DataFrame usando la máscara de la planta
        resultados.extend(dataframe.loc[mask, 'Planta '].tolist())
        #Elimino duplicados
        sin_duplicados = set(resultados)
    return sin_duplicados


ruta_archivo = r'C:\Users\Juan José Valemcia M\Desktop\Articulos Tesisi\Sistema experto plantas\Sistema-experto-plantas-medicinales\serpm\Plantas_propiedades_arr.csv' 
df = pd.read_csv(ruta_archivo)
lista_busqueda =['triterpenos']
resultado= buscar_valores(df, lista_busqueda)
print(resultado)


