from strategies import estrategias
from utils.operacionesDataframe import eliminarColumnasNulas, formatearColumnasDatetime
from database.consultas import consultar_ventas_e_inventario
import logging

def obtener_dataframe(table_name):
    try:
        estrategia = estrategias.get(table_name)
        if not estrategia:
            raise ValueError(f"No se encontró una estrategia para la tabla '{table_name}'.")
        df = estrategia()
        df = eliminarColumnasNulas(df)
        df = formatearColumnasDatetime(df)
        logging.info(f'Información convertida en dataframe con éxito')
        return df
    except Exception as e:
        logging.error(f"Error al obtener la estrategia o consultar los datos: {e}")
        return None
    
def obtener_dataframe_join():
    return consultar_ventas_e_inventario()