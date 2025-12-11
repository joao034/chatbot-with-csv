import pandas as pd

# Método para convertir resultados de una consulta SQL a DataFrame. 
def resultados_a_dataframe( resultados, columnas ):
    if resultados is None or columnas is None:
        print("No hay resultados o columnas para convertir en DataFrame")
        return None
    return pd.DataFrame(resultados, columns=columnas)

"""Formatea todas las columnas de tipo datetime de un DataFrame al formato 'Y-M-D h:m:s'.
    Las fechas incompletas se completan con '00:00:00'. """
def formatearColumnasDatetime(df, formato='%Y-%m-%d %H:%M:%S'):
    df_resultado = df.copy()

    # Iterar por columnas de tipo datetime
    for columna in df.select_dtypes(include=['datetime64[ns]']).columns:
        try:
            # Aplicar el formato deseado y reconvertir a datetime
            df_resultado[columna] = pd.to_datetime(
                df_resultado[columna].dt.strftime(formato)
            )
        except Exception as e:
            print(f"No se pudo formatear la columna '{columna}': {e}")
    
    return df_resultado

def eliminarColumnasNulas( df ):
    return df.dropna( axis=1, how='all')

def obtener_columnas_string(df):
    cols = list(df.columns)
    cols = ', '.join(cols)
    return cols

def read_csv( ruta ):
    try:
        return pd.read_csv(ruta)
    except FileNotFoundError:
        print(f"Error: File '{ruta} not found'")
        return None

    