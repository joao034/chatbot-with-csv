# Funciones para cada consulta de tabla
from utils.operacionesDataframe import read_csv
import os

def consultar_ventas_e_inventario( ):
    return read_csv( os.getenv('JOIN_VENTAS_INVENTARIO_CSV_PATH'))