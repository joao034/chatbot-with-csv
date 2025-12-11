from utils.operacionesDataframe import read_csv
import os

def consultar_inventario ():
    return read_csv( ruta = os.getenv('INVENTARIO_CSV_PATH'))