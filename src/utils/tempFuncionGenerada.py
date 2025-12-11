
import pandas as pd
import numpy as np
import re

def motivos_clientes_suzuki_no_vienen_mantenimiento(df: pd.DataFrame) -> dict:
    try:
        # Validar que df es un DataFrame y tiene las columnas necesarias
        required_columns = {'purchase_int', 'marca', 'country', 'comentario'}
        if not isinstance(df, pd.DataFrame):
            return {'Error': 'El parámetro no es un DataFrame'}
        if not required_columns.issubset(df.columns):
            return {'Error': f'Faltan columnas requeridas: {required_columns - set(df.columns)}'}

        # Filtrar por purchase_int = True, marca Suzuki y country Ecuador
        df_filtered = df[
            (df['purchase_int'] == True) &
            (df['marca'].str.contains(r'\bsuzuki\b', regex=True, case=False, na=False)) &
            (df['country'].str.contains(r'\becuador\b', regex=True, case=False, na=False))
        ]

        if df_filtered.empty:
            return {'motivos': False}

        # Palabras clave para buscar comentarios negativos o quejas relacionadas con mantenimiento
        palabras_clave = [
            r'insatisfacci.n', r'mal servicio', r'precio(s)? alto(s)?', r'demora(s)?',
            r'mala atenci.n', r'falta de confianza', r'queja', r'insatisfacci.n general',
            r'costos altos', r'tiempo de espera', r'personal no profesional', r'calidad baja',
            r'repuestos limitados', r'atenci.n deficiente', r'problemas con repuestos',
            r'no confiable', r'caro', r'costoso', r'ineficiente', r'fallas en servicio'
        ]
        regex_palabras = '|'.join(palabras_clave)

        # Filtrar comentarios que contengan alguna de las palabras clave
        df_comentarios = df_filtered[
            df_filtered['comentario'].str.contains(regex_palabras, regex=True, case=False, na=False)
        ]

        if df_comentarios.empty:
            return {'motivos': False}

        # Categorizar comentarios según motivos
        categorias = {
            'Percepción de precios altos': [
                r'precio(s)? alto(s)?', r'costos altos', r'caro', r'costoso'
            ],
            'Tiempos de espera prolongados': [
                r'demora(s)?', r'tiempo de espera', r'ineficiente'
            ],
            'Calidad del servicio recibido': [
                r'mal servicio', r'calidad baja', r'insatisfacci.n general', r'insatisfacci.n',
                r'atenci.n deficiente', r'fallas en servicio'
            ],
            'Disponibilidad limitada de repuestos': [
                r'repuestos limitados', r'problemas con repuestos'
            ],
            'Falta de profesionalismo del personal': [
                r'falta de confianza', r'personal no profesional', r'no confiable', r'mala atenci.n'
            ]
        }

        motivos_dict = {cat: [] for cat in categorias}

        # Clasificar cada comentario en las categorías según coincidencias
        for _, row in df_comentarios.iterrows():
            comentario = row['comentario']
            comentario_lower = comentario.lower()
            asignado = False
            for categoria, patrones in categorias.items():
                for patron in patrones:
                    if re.search(patron, comentario_lower, re.IGNORECASE):
                        motivos_dict[categoria].append(comentario)
                        asignado = True
                        break
                if asignado:
                    break
            # Si no se asignó a ninguna categoría, no se incluye

        # Eliminar categorías vacías
        motivos_dict = {k: v for k, v in motivos_dict.items() if v}

        if not motivos_dict:
            return {'motivos': False}

        return {'motivos': motivos_dict}

    except Exception as e:
        return {'Error': str(e)}
