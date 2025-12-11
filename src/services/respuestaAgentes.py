
import logging, ast

from agentes import (
    agenteIntencion,
    agenteHumanizacion,
    agenteRespuestaAmigable,
    agenteDecisionTabla,
    agenteAnalizaContexto
)

def obtener_intencion(prompt):
    try:
        intencion = agenteIntencion.tieneIntencionConLaBD(prompt)
        logging.info(f'Intencion: {intencion}')
        return ast.literal_eval(intencion)
    except Exception as e:
        logging.error(f"Error al determinar la intención: {e}")
        return None 
    
def humanizar_respuesta(respuesta):
    try:
        humanizada = agenteHumanizacion.humanizarRespuesta(respuesta)
        logging.info(f'Respuesta humanizada generada.')
        return humanizada
    except Exception as e:
        logging.error(f"Error al humanizar la respuesta: {e}")
        return "Ocurrió un error al procesar tu solicitud."
    
def hacer_respuesta_amigable(prompt_intent, respuesta_humanizada):
    try:
        amigable = agenteRespuestaAmigable.obtenerRespuestaAmigable(prompt_intent, respuesta_humanizada)
        logging.info(f'Respuesta amigable generada.')
        return amigable
    except Exception as e:
        logging.error(f"Error al generar respuesta amigable: {e}")
        return "Ocurrió un error al procesar tu solicitud."
    
def obtener_nombres_tablas(prompt_intent):
    try:
        nombres_tablas = agenteDecisionTabla.obtenerNombreTabla(prompt_intent)
        logging.info(f'Nombres de tablas: {nombres_tablas}')
        return ast.literal_eval(nombres_tablas)
    except Exception as e:
        logging.error(f"Error al obtener nombres de tablas: {e}")

def obtener_contexto(prompt_intent, chat_history):
    try:
        prompt_enriquecido = agenteAnalizaContexto.analizeContext(prompt_intent, chat_history)
        logging.info(f'Prompt con contexto obtenido')
        return prompt_enriquecido
    except Exception as e:
        logging.error(f"Error al obtener el contexto: {e}")
        return None