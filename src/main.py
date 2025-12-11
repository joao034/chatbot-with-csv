import chainlit as cl
import logging

from services.respuestaAgentes import (
    obtener_intencion,
    obtener_nombres_tablas,
    obtener_contexto,
    humanizar_respuesta,
    hacer_respuesta_amigable
)

from services.resultadosFuncion import (
    manejar_consulta_compleja,
    manejar_consulta_simple
)

from services.obtenerDataframe import (
    obtener_dataframe, 
    obtener_dataframe_join
)


# Configuración del logger
logging.basicConfig(
    level=logging.ERROR,  # Nivel mínimo de logs que se registrarán
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato del log
)


def get_mensaje_inicial():
    tablas = "inventario y ventas"
    return f"¡Hola! Hazme una pregunta respecto al {tablas} de tu empresa."


async def enviar_mensaje_usuario( mensaje ):
    msg = cl.Message(content=mensaje)
    await msg.send() 

# Función principal
@cl.on_message
async def main(message: cl.Message):
    
    chat_history = cl.user_session.get('chat_history')
    prompt_intent = message.content

    try:
        prompt_enriquecido = prompt_intent
        if( chat_history ):
             prompt_enriquecido = await cl.make_async(obtener_contexto)(prompt_intent, chat_history)

        chat_history.append({'role': 'user', 'content': prompt_enriquecido})

        intencion = await cl.make_async(obtener_intencion)(prompt_enriquecido)

        if not intencion : 
            await enviar_mensaje_usuario(get_mensaje_inicial())
            return
        
        await enviar_mensaje_usuario("Consultando información, puede tardar unos minutos...")

        nombres_tablas = await cl.make_async(obtener_nombres_tablas)(prompt_enriquecido)
        if not nombres_tablas:
            await enviar_mensaje_usuario("No se pudieron determinar las tablas requeridas.")
            return

        if len(nombres_tablas) > 1:
            df = await cl.make_async(obtener_dataframe_join)()
            
            if df is None:
                return await message_df_empty() 
            
            respuesta_generada = await cl.make_async(manejar_consulta_compleja)(df, prompt_enriquecido)
        else:
            df = await cl.make_async(obtener_dataframe)( nombres_tablas[0] )

            if df is None:
                return await message_df_empty() 

            respuesta_generada = await cl.make_async(manejar_consulta_simple)(df, prompt_enriquecido)

        chat_history.append({'role': 'assistant', 'content': respuesta_generada})

        respuesta_humanizada = await cl.make_async(humanizar_respuesta)(respuesta_generada)

        respuesta_amigable = await cl.make_async(hacer_respuesta_amigable)(prompt_enriquecido, respuesta_humanizada)

        await enviar_mensaje_usuario(respuesta_amigable)
  
    except Exception as e:
        logging.error(f"Error inesperado en la aplicación: {e}")
        await enviar_mensaje_usuario("Ocurrió un error inesperado. Por favor, contacta al administrador.")

async def message_df_empty():
    await enviar_mensaje_usuario("No existen datos para consultar.")
    return

@cl.on_chat_start
async def on_chat_start():

    await enviar_mensaje_usuario(get_mensaje_inicial())

    cl.user_session.set('chat_history', [])

