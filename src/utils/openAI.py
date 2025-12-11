from openai import OpenAI
from dotenv import load_dotenv
import os

# Carga las variables de entorno
load_dotenv()

# Inicializa el cliente de OpenAI
client = OpenAI(api_key=os.getenv('API_OPENAI_KEY'))

def use_gpt_api(messages, model="gpt-4o-mini", temperature=0.0, max_tokens=500):
    """
    Interactúa con la API de OpenAI GPT para generar respuestas basadas en los mensajes proporcionados.

    Args:
        messages (list): Lista de mensajes en formato [{"role": "system|user|assistant", "content": "mensaje"}].
        model (str): Modelo de OpenAI a utilizar (por ejemplo, "gpt-4").
        temperature (float): Nivel de aleatoriedad en las respuestas generadas (0.0 para respuestas más determinísticas).
        max_tokens (int): Número máximo de tokens para la respuesta generada.

    Returns:
        str: Respuesta generada por GPT.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error al interactuar con la API de OpenAI: {str(e)}"
