
import importlib, inspect, os, logging
from .operacionesArchivo import guardarArchivo, eliminarArchivo

#Carga y devuelve un módulo temporal desde un archivo específico.
def crearModuloTemporal(path):
    
    spec = importlib.util.spec_from_file_location("tempFuncionGenerada", path)
    temp_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(temp_module)
    return temp_module

#Ejecuta la única función dentro de un módulo dado usando un DataFrame.
def ejecutarFuncionModulo(moduloTemporal, df):

    funciones = [func for _, func in inspect.getmembers(moduloTemporal, inspect.isfunction)]
    if funciones:
        return funciones[0](df)  # Ejecuta la primera función con el DataFrame
    return None

def procesar_funcion_temporal(df, funcion):
    path = os.path.join(os.path.dirname(__file__), 'tempFuncionGenerada.py')
    try:
        logging.info('Ejecutando la funcion...')
        guardarArchivo(path, funcion)
        modulo_temporal = crearModuloTemporal(path)
        respuesta = ejecutarFuncionModulo(modulo_temporal, df)

        logging.info(f'Funcion ejecutada con exito.')

        if respuesta is None:
            raise RuntimeError("No se encontró la función en el módulo temporal.")

        return respuesta
    except Exception as e:
        logging.error(f"Error al procesar la función temporal: {e}")
        return None
    finally:
        eliminarArchivo(path)
