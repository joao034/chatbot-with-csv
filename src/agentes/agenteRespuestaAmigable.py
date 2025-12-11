from utils import openAI

def obtenerRespuestaAmigable( prompt_intent, respuestaHumanizada ):
    
    system = "La unidad monetaria es el dólar estadounidense (USD). Agrega el símbolo $ antes de la cantidad para indicar que estás hablando en dólares. Por ejemplo, $100.00."
    
    user = f"""
    Responde la pregunta del usuario y transforma la respuesta para que suene más amigable y cercana, adaptándote al estilo de lenguaje del usuario original. 

    Objetivos:
    - Usa un tono cálido y conversacional
    - Mantén la esencia del mensaje original

    Pregunta del usuario: {prompt_intent}
    Respuesta que debes hacer amigable: {respuestaHumanizada}

    Devuelve una respuesta amigable"""
    
    messages = [
        { "role": "system", "content": system},
        {"role": "user", "content": user}
    ]

    return openAI.use_gpt_api(messages, max_tokens=900)