import datetime
import os

def registrar_log(nombre, idioma, consulta, respuesta):
    """
    Registra una entrada de conversación del asistente en un archivo de log.

    Parámetros:
    - nombre (str): Nombre del personaje que responde (e.g., "nala", "otto").
    - idioma (str): Idioma utilizado en la interacción (e.g., "es", "en", "pt").
    - consulta (str): Pregunta o entrada del usuario.
    - respuesta (str): Respuesta generada por el asistente.

    Crea el archivo 'logs/registro.txt' si no existe y agrega la entrada con timestamp.
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{fecha}] Personaje: {nombre} | Idioma: {idioma} | Pregunta: {consulta} | Respuesta: {respuesta}\n"

    os.makedirs("logs", exist_ok=True)
    with open("logs/registro.txt", "a", encoding="utf-8") as archivo:
        archivo.write(log_entry)
