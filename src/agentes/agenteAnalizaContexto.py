from utils import chatFormatter, openAI

def analizeContext(prompt, chat_history):
    
    formatted_history = chatFormatter.format_chat_history(chat_history, num_messages=4)

    system_prompt = f"""
        Eres un asistente experto en análisis de contexto conversacional.
        Tu tarea es:
        1. Analizar la última pregunta del usuario y el historial de la conversación
        2. Determinar si la pregunta necesita contexto adicional
        3. Si lo necesita, reformular la pregunta incluyendo el contexto relevante
        4. Si no lo necesita, devolver la pregunta original
        
        Ejemplos de contexto:
        - Referencias implícitas a elementos mencionados antes
        - Continuación de consultas anteriores
        - Modificaciones de consultas previas
    """

    user_prompt = f"""
        Historial de la conversación:
        {formatted_history}
        
        Nueva pregunta del usuario: {prompt}
        
        Reformula la pregunta incluyendo el contexto necesario si hace falta.
        Si no necesita contexto adicional, devuelve la pregunta original. """
    
    messages = [
        { "role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    return openAI.use_gpt_api(messages, max_tokens=800)

   