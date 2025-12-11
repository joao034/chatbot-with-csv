def format_chat_history(chat_history, num_messages=4):
    """
    Formatea el historial de chat, mostrando los últimos 'num_messages' mensajes.
    
    Args:
        chat_history (list): Lista de diccionarios con claves 'role' y 'content'.
        num_messages (int): Número de mensajes del final del historial que se incluirán.

    Returns:
        str: El historial formateado como un string.
    """
    formatted_history = "\n".join([
        f"{'Usuario' if msg['role'] == 'user' else 'Asistente'}: {msg['content']}"
        for msg in chat_history[-num_messages:]
    ])
    return formatted_history