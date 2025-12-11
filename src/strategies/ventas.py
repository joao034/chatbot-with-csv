from utils.operacionesDataframe import read_csv
import os

def consultar_ventas():
    return read_csv( ruta = os.getenv('VENTAS_CSV_PATH'))
