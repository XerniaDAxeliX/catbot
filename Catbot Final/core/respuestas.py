import json

import json

def leer_json(path):
    """
    Lee un archivo JSON que contiene una lista de preguntas y respuestas.

    Args:
        path (str): Ruta del archivo JSON.

    Returns:
        list[tuple[str, str]]: Lista de tuplas (pregunta, respuesta).
    """
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return [(item["pregunta"], item["respuesta"]) for item in datos]
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"⚠️ Error al leer el archivo: {path}")
        return []


def escribir_json(path, datos):
    """
    Escribe una lista de preguntas y respuestas en formato JSON.

    Args:
        path (str): Ruta del archivo de salida.
        datos (list[tuple[str, str]]): Lista de tuplas (pregunta, respuesta).
    """
    try:
        estructura = [{"pregunta": p, "respuesta": r} for p, r in datos]
        with open(path, "w", encoding="utf-8") as archivo:
            json.dump(estructura, archivo, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Error al escribir el archivo: {e}")