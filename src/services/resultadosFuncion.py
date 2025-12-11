from utils.operacionesDataframe import obtener_columnas_string
from agentes import agenteGeneraFuncion
import logging
from utils.moduloTemporal import procesar_funcion_temporal

def manejar_consulta_compleja(df, prompt_intent):
    try:
        cols = obtener_columnas_string(df)
        funcion = agenteGeneraFuncion.generarFuncionParaConsultaCompleja(cols, prompt_intent)
        logging.info('Funcion generada.')
        return procesar_funcion_temporal(df, funcion)
    except Exception as e:
        logging.error(f"Error al procesar la consulta simple: {e}")
        return None
    
def manejar_consulta_simple(df, prompt_intent):
    try:
        cols = obtener_columnas_string(df)
        funcion = agenteGeneraFuncion.generarFuncionParaConsultaSimple(cols, prompt_intent)
        logging.info('Funcion generada.')
        return procesar_funcion_temporal(df, funcion)
    except Exception as e:
        logging.error(f"Error al procesar la consulta simple: {e}")
        return None