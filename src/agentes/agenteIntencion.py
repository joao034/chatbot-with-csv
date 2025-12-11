from utils import openAI

def tieneIntencionConLaBD( prompt_intent ):

    system = """Detecta si el usuario está haciendo una pregunta sobre inventario o ventas de una empresa de venta de vehículos . 
                Devuelve un string, 'True' si es positivo, 'False' si es negativo. """

    messages = [
        { "role": "system", "content": system},
        {"role": "user", "content": prompt_intent}
    ]

    return openAI.use_gpt_api(messages, model="gpt-3.5-turbo-0125", max_tokens=10)