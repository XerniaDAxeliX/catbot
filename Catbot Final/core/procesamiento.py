import difflib
import unicodedata
import string
import re

# Stopwords mínimas por idioma (podés expandir)
STOPWORDS_ES = {"que", "como", "donde", "cual", "cuales", "cuanto", "cuantos", "para", "es", "la", "el"}
STOPWORDS_EN = {"what", "how", "where", "which", "who", "whom", "the", "is", "are", "can"}
STOPWORDS_PT = {"que", "como", "onde", "qual", "quais", "quanto", "quantos", "para", "é", "o", "a"}

IDIOMA_STOPWORDS = {
    "es": STOPWORDS_ES,
    "en": STOPWORDS_EN,
    "pt": STOPWORDS_PT,
}

def limpiar_texto(texto, idioma):
    """
    Aplica limpieza avanzada al texto: reemplaza comillas, guiones, contracciones,
    elimina caracteres invisibles, tildes, stopwords y puntuación.

    Args:
        texto (str): Texto a limpiar.
        idioma (str): Idioma del texto ("es", "en", "pt").

    Returns:
        str: Texto limpio y estandarizado.
    """
    # Reemplazo de comillas tipográficas y guiones
    texto = texto.replace("’", "'").replace("‘", "'")
    texto = texto.replace('“', '"').replace('”', '"')
    texto = texto.replace("–", "-").replace("—", "-").replace("−", "-")

    # Reemplazo de contracciones (sólo inglés)
    if idioma == "en":
        contracciones = {
            "can't": "cannot",
            "won't": "will not",
            "i'm": "i am",
            "you're": "you are",
            "it's": "it is",
            "they're": "they are",
            "let's": "let us"
        }
        for contra, expandida in contracciones.items():
            texto = texto.replace(contra, expandida)

    # Eliminación de caracteres invisibles
    texto = re.sub(r'[\u200B\u200C\u200D\uFEFF]', '', texto)

    # Normalización unicode y eliminación de tildes
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto.lower())
        if unicodedata.category(c) != 'Mn'
    )

    # Eliminación de puntuación final
    texto = texto.strip().rstrip('?.!')

    # Eliminación de puntuación intermedia
    texto = texto.translate(str.maketrans('', '', string.punctuation))

    # Eliminación de stopwords
    stopwords = IDIOMA_STOPWORDS.get(idioma, set())
    palabras = texto.split()
    texto = ' '.join([p for p in palabras if p not in stopwords])

    return texto

def stem_text(texto, stemmer, idioma):
    """
    Normaliza, limpia y aplica stemming a un texto dado.

    Args:
        texto (str): Texto original.
        stemmer (SnowballStemmer): Objeto de stemming del idioma.
        idioma (str): Idioma del texto ("es", "en", "pt").

    Returns:
        str: Texto procesado con palabras en su forma raíz.
    """
    texto = limpiar_texto(texto, idioma)
    palabras = [p for p in texto.split() if p.isalnum()]
    return " ".join(stemmer.stem(p) for p in palabras)

def calcular_similitud(pregunta_usuario, pregunta_base, stemmer, idioma):
    """
    Calcula un score de similitud entre dos preguntas, combinando ratio y coincidencias.

    Args:
        pregunta_usuario (str): Pregunta del usuario.
        pregunta_base (str): Pregunta de la base.
        stemmer (SnowballStemmer): Stemmer del idioma.
        idioma (str): Idioma actual ("es", "en", "pt").

    Returns:
        float: Score de similitud entre 0 y 1.
    """
    stem_usuario = stem_text(pregunta_usuario, stemmer, idioma)
    stem_base = stem_text(pregunta_base, stemmer, idioma)
    ratio = difflib.SequenceMatcher(None, stem_usuario, stem_base).ratio()
    interseccion = set(stem_usuario.split()) & set(stem_base.split())
    score = ratio * 0.7 + len(interseccion) * 0.3 / (len(stem_usuario.split()) + 1)
    return score

def buscar_respuesta_exacta(consulta, datos):
    """
    Busca si existe una pregunta exactamente igual (normalizada) en la base.
    Retorna la respuesta si la encuentra, o None.

    Args:
        consulta (str): Pregunta del usuario.
        datos (list): Lista de (pregunta, respuesta) base.

    Returns:
        str | None: Respuesta correspondiente o None si no hay match exacto.
    """
    normalizada = limpiar_texto(consulta, "es")  # suposición por defecto, si hace falta usar idioma real se ajusta
    for pregunta, respuesta in datos:
        if limpiar_texto(pregunta, "es") == normalizada:
            return respuesta
    return None