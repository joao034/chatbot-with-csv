from utils import openAI

def humanizarRespuesta( outcome ):

    system = "Eres un comunicador entre resultados de funciones de data science y un humano"

    messages = [
        { "role": "system", "content": system},
        {"role": "user", "content": str(outcome)}
    ]

    return openAI.use_gpt_api(messages, max_tokens=900)