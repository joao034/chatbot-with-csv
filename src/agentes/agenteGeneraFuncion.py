from utils import openAI

colsVentas = """
    -'FECHA' : corresponde a la fecha de la venta.
    -'CANTIDAD' : cantidad de 'VENTA' o 'DEVOLUCION', siempre es 1 o -1.
    -'TIPODOCUMENTO' : detalle de la transación, si es una 'VENTA' o una 'DEVOLUCION'.
    -'CLIENTE' : nombre del cliente.
    -'EDAD' : edad del cliente.
    -'CIUDAD' : ciudad del cliente.
    -'PROVINCIA' : provincia del cliente.
    -'ACTIVIDAD_ECONOMICA' : actividad economica del cliente.
    -'VENDEDOR' : nombre del vendedor.
    -'FACTURA' : número de factura.
"""

colsInventario = """
    -'ESTADO' : corresponde al estado del vehiculo. Contiene los siguientes estados: (DISPONIBLE, DISPONIBLE RESERVADO, PDI, TRANSITO, TRANSITO RESERVADO), a contuación su significado:
                *'DISPONIBLE': disponible para venta.
                *'DISPONIBLE RESERVADO': qué un vehículo ya esta reservado para venta y no se lo puede tomar.
                *'PDI': se encuentra en preparación para pasar a 'DISPONIBLE'.
                *'TRANSITO': qué fue pedido a fábrica.
                *'TRANSITO RESERVADO': qué el pedido a fábrica se encuentra reservado para que al llegar sea entregado al cliente.
    -SUBSEGMENTO: subsegmento del vehiculo: ('LIVIANO', 'PESADO', 'TRACTO', 'VOLQUETA').
    -'COLOR' : color del vehiculo.
    -'PRECIO' : precio del vehiculo.
    -'UBICACION': ubicación dentro de cada agencia donde se encuentra el vehículo.
    -'EXISTENCIA' : cantidad de existencias (stock).
    -'F_ESTIMADA' : Fecha estimada de arribo, únicamente para inventario en estado en TRANSITO y TRANSITO RESERVADO.
"""

colsComunes = """
        -'CHASIS' : número de chasis del vehiculo.
        -'MODELO' : modelo del vehiculo.
        -'MARCA' : marca del vehiculo.
        -'AGENCIA': agencia donde se encuentra el vehículo.
        -'ANIO' : año del vehiculo.
        -'SEGMENTO' : segmento del vehiculo: ('LIVIANO', 'PESADO', 'MAQUINARIA').
        -'MOTOR' : motor del vehiculo.
        -'MODELO_HOMOLOGADO': modelo homologado del vehiculo.
"""

def generarFuncionParaConsultaSimple( columns, prompt_intent ): 

    system = f"""Eres un data scientsit que sólo escribe funciones de python para df que es un Pandas DataFrame 
    que tiene específicamente estas columnas : {columns}, con las cuales debes generar la función. 
    
    Requisitos para la función:

    1. Componentes Obligatorios:
    - La funcion recibe un único parámetro, el dataframe.
    - Importar unicamente las librerías necesarias, por ejemplo: pandas, numpy
    - Implementar validaciones previas
    - Manejar excepciones específicas
    - No agregar ejemplo de uso
    - Asegúrate de usar pandas y devolver resultados claros
    - A todas las preguntas relacionadas con ventas debes restar las devoluciones. Es decir no debes agregar esta comparación: df[df['TIPODOCUMENTO'] == 'VENTA']
    
    2. Consideraciones:
    - Considera la columna 'ANIO' para preguntas relacionadas unicamente con el año del modelo del vehiculo. Para preguntas relacionadas con el año de la venta, considera la columna 'FECHA'. 
    - Si la pregunta se refiere a inventario, por ejemplo el número de unidades en inventario, debes sumar las existencias, especificadas en el campo 'EXISTENCIA'.
    - Si el usuario realiza una pregunta que involucra el cálculo del total, asegúrate de considerar las devoluciones. 
        Las devoluciones están identificadas por el campo 'TIPODOCUMENTO' con el valor 'DEVOLUCION', donde si es una devolución el campo total de 
        contiene un valor negativo. Por lo tanto:
        1. Suma todos los valores del campo total, asegurándote de incluir los valores negativos de las devoluciones para reflejar su impacto.
        2. Devuelve el total ajustado, considerando tanto los valores positivos como los negativos.

    - Si la pregunta involucra ventas, siempre debes considerar las devoluciones, es decir si hubieron 100 ventas pero 10 devoluciones, entonces el número total de 
        ventas será 90. Para esto utiliza el campo 'TIPODOCUMENTO'.
        
    3. Salida consistente:
    Diccionario de salida con:
        * Resultados principales

    4. Información de contexto:
    Las columnas pueden pertencer a estas tablas:
    Ventas: {colsVentas}
    Inventario: { colsInventario }

    Ambas tablas comparten las siguientes columnas: {colsComunes}
        
    Genera una función que responda a la solicitud del usuario y devuelve el diccionario con los resultados."""

    messages = [
        { "role": "system", "content": system},
        {"role": "user", "content": prompt_intent}
    ]

    response = openAI.use_gpt_api(messages, model="gpt-4-turbo", max_tokens=600)

    return response.split('```')[1].replace('python','')

def generarFuncionParaConsultaCompleja( columns, prompt_intent ): 

    system = f"""
    
    Eres un data scientsit que sólo escribe funciones de python que interactua con un dataframe con las siguientes columnas: 
    {columns}, con las cuales debes generar una función para responder a la pregunta del usuario. 
    
    Requisitos para la función:

    1. Componentes Obligatorios:
    - La funcion recibe un único parámetro, el dataframe
    - Importar unicamente las librerías necesarias, por ejemplo: pandas, numpy
    - Implementar validaciones previas
    - Manejar excepciones específicas
    - No agregar ejemplo de uso
    - Asegúrate de usar pandas y devolver resultados claros

    2. Consideraciones:
    - El parametro es un dataframe que contiene registros de ventas e items de un inventario.
    - Es un dataframe inconsistente, ya que fue construido a traves de un full outer join entre dos tablas. Entonces algunos campos son nulos/vacios.
    - Si la pregunta se refiere a inventario, por ejemplo el número de unidades en inventario, debes sumar las existencias, especificadas en el campo 'EXISTENCIA'.
    - Considera la columna 'ANIO' para preguntas relacionadas unicamente con el año del modelo del vehiculo. Para preguntas relacionadas con el año de la venta, considera la columna 'FECHA'. 
    - Si el usuario realiza una pregunta que involucra el cálculo del total, asegúrate de considerar las devoluciones. 
        Las devoluciones están identificadas por el campo tipoDocumento con el valor 'DEVOLUCION', y el campo total de 
        dichas devoluciones contiene un valor negativo. Por lo tanto:
        1. Suma todos los valores del campo total, asegurándote de incluir los valores negativos de las devoluciones para reflejar su impacto.
        2. Devuelve el total ajustado, considerando tanto los valores positivos como los negativos.
    - Si la pregunta involucra ventas, siempre debes considerar las devoluciones, es decir si hubieron 100 ventas pero 10 devoluciones, entonces el número total de 
        ventas será 90. Para esto utiliza el campo 'TIPODOCUMENTO'.
    - La columna 'TOTAL' solo esta llena cuando se trata de una venta. Por lo tanto, cuando la pregunta involucra una venta, por ejemplo hacer una venta proyectada,
      solo se deben tomar los registros que tienen un valor en la columna 'TOTAL'. 
    - La columna 'EXISTENCIA' solo esta llena cuando se trata de un registro que está en inventario. Por lo tanto, cuando la pregunta involucra inventario, por ejemplo
      la cantidad de stock de un modelo, solo se deben tomar los registros que tienen un valor en la columna 'EXISTENCIA'. 
    - **Cuando la pregunta involucra un conteo de existencias o stock**, debes eliminar registros duplicados de 'CHASIS' y 'EXISTENCIA' para evitar que un mismo vehículo sea contado más de una vez.
    - Asegúrate de que los resultados sean coherentes con el contexto. Por ejemplo, si se solicita el stock proyectado de un modelo de vehículo para el próximo mes, no tiene sentido devolver un número decimal, 
      ya que el stock debe ser un número entero. Sin embargo, si se pregunta por el total de ventas esperadas para el próximo año, un número decimal sería apropiado.

    3. Salida Consistente:
    - Diccionario de salida con:
        * Resultados principales

    4. Información de contexto:
        Las columnas pertencen a dos tablas:
        Ventas: {colsVentas}
        Inventario: { colsInventario}
    Genera una función que responda a la solicitud del usuario y devuelve el diccionario con los resultados."""
    
    messages = [
        { "role": "system", "content": system},
        {"role": "user", "content": prompt_intent}
    ] 

    response = openAI.use_gpt_api(messages, model="gpt-4-turbo", max_tokens=800)
    return response.split('```')[1].replace('python','')