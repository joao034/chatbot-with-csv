from utils import openAI

def obtenerNombreTabla( prompt_intent ):
    tableNames = ["ventas", "inventario"]

    system_prompt = f"""
    Dispones de las siguientes tablas: {tableNames}. Analiza la pregunta del usuario y devuelve un arreglo 
                con los nombres de las tablas que son relevantes para responder a la pregunta. 
                Si la pregunta está relacionada con una sola tabla, devuelve un arreglo con el nombre de esa tabla, por ejemplo: ['ventas']. 
                Si la pregunta involucra múltiples tablas, devuelve un arreglo con los nombres de todas las tablas necesarias, 
                por ejemplo: ['ventas', 'inventario'].
                No incluyas tablas innecesarias en la respuesta.
                """
    
    messages = [
        { "role": "system", "content": system_prompt},
        {"role": "user", "content": prompt_intent}
    ]

    return openAI.use_gpt_api( messages, max_tokens=50 )