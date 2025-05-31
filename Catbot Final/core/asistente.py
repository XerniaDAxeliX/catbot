import random
from core.respuestas import leer_json
from core.idiomas import IDIOMAS, ARCHIVOS, stemmer_por_idioma
from core.procesamiento import calcular_similitud, buscar_respuesta_exacta
from core.promedios import calcular_promedio
from core.log import registrar_log

SALIDAS_VALIDAS = ["salir", "exit", "quit", "chau", "chao", "adios", "bye"]

PALABRAS_PROMEDIO = [
    "promedio", "promediar", "promedia", "promediame", "media", "média",
    "calcular media", "average", "avg", "compute average"
]

PALABRAS_AYUDA = [
    "ayuda", "help", "ajuda", "ajudar", "assistência"
]

def contiene_palabra_clave(consulta, lista):
    """
    Verifica si alguna palabra clave está presente en la consulta del usuario.

    Parámetros:
    - consulta (str): Texto ingresado por el usuario.
    - lista (list[str]): Lista de palabras clave a buscar.

    Retorna:
    - bool: True si alguna palabra de la lista está dentro de la consulta, False si no.
    """
    consulta_limpia = consulta.lower()
    return any(palabra in consulta_limpia for palabra in lista)

def elegir_idioma():
    """
    Permite al usuario seleccionar un idioma para interactuar con el chatbot.

    Muestra las opciones disponibles (español, inglés, portugués) y valida la entrada.

    Retorna:
    - str: Código del idioma seleccionado ("es", "en", "pt").
    """
    print("🌐 Elegí un idioma:")
    print("1) Miauspañol\n2) Meownglish\n3) Miautuguês")

    while True:
        opcion = input("> ").strip()
        if opcion == "1":
            return "es"
        elif opcion == "2":
            return "en"
        elif opcion == "3":
            return "pt"
        else:
            print("Opción inválida. Probá de nuevo.")



def elegir_personaje(idi):
    """
    Permite al usuario seleccionar un personaje (Nala, Luigi u Otto).

    Muestra las opciones disponibles usando los textos del diccionario de idioma (`idi`) y
    valida la entrada hasta que el usuario elija una opción válida.

    Parámetros:
    - idi (dict): Diccionario de idioma con los textos de interfaz traducidos.

    Retorna:
    - str: Nombre del personaje seleccionado ("nala", "luigi", "otto").
    """
    print(idi["elige_opcion"])
    print(idi["opciones_gatos"])

    while True:
        opcion = input("> ").strip()
        if opcion == "1":
            return "nala"
        elif opcion == "2":
            return "luigi"
        elif opcion == "3":
            return "otto"
        else:
            print(idi["opcion_invalida"])


def obtener_respuesta(consulta, datos, nombre, stemmer, idioma, idi, archivo):
    """
    Busca la respuesta adecuada a una consulta dada. Intenta primero una coincidencia exacta,
    luego por similitud, y si no hay coincidencias suficientes, sugiere posibles preguntas
    similares o permite al usuario enseñar una nueva respuesta.

    Parámetros:
    - consulta (str): La pregunta escrita por el usuario.
    - datos (list): Lista de tuplas (pregunta, respuesta) cargadas desde el archivo JSON.
    - nombre (str): Nombre del personaje seleccionado (nala, luigi u otto).
    - stemmer (obj): Objeto SnowballStemmer para recortar palabras a su raíz.
    - idioma (str): Código del idioma actual ("es", "en", "pt").
    - idi (dict): Diccionario de idioma con los textos traducidos.
    - archivo (str): Nombre del archivo JSON actual donde se guardan los datos.

    Retorna:
    - str: La respuesta seleccionada o aprendida para mostrar al usuario.
    """

    # 1. Intenta encontrar una coincidencia exacta
    respuesta_exacta = buscar_respuesta_exacta(consulta, datos)
    if respuesta_exacta:
        return respuesta_exacta

    # 2. Calcula similitudes con todas las preguntas
    puntuadas = []
    for pregunta, respuesta in datos:
        score = calcular_similitud(consulta, pregunta, stemmer, idioma)
        puntuadas.append((score, pregunta, respuesta))

    # Ordena las coincidencias por puntaje de similitud (de mayor a menor)
    puntuadas.sort(reverse=True)

    # 3. Si hay una coincidencia suficientemente buena, devuelve esa respuesta
    if puntuadas and puntuadas[0][0] >= 0.55:
        return puntuadas[0][2]  # respuesta con mayor similitud

    # 4. Si no hay buena coincidencia, sugiere hasta 3 preguntas similares
    sugerencias = puntuadas[:3]
    print(random.choice(idi["frases_no_se"]))  # frase simpática de “no sé”

    if sugerencias:
        print(f"{idi['tal_vez_quisiste']}")
        for idx, (_, pregunta, _) in enumerate(sugerencias, 1):
            print(f"{idx}) {pregunta}")
        print("0) Otra / No es ninguna")

        # 5. Permite elegir una sugerencia o enseñar una nueva pregunta/respuesta
        while True:
            opcion = input("> ").strip()
            if opcion == "0":
                # El usuario enseña una nueva pregunta/respuesta
                nueva_pregunta = input("🔧 Escribí tu pregunta como te gustaría que el bot la entienda: ").strip().lower()
                nueva_respuesta = input("📝 ¿Qué debería responder el bot?: ").strip()
                nueva_entrada = {"pregunta": nueva_pregunta, "respuesta": nueva_respuesta}

                # Agrega la nueva entrada a la lista en memoria
                datos.append((nueva_pregunta, nueva_respuesta))

                # Guarda la nueva entrada en el archivo JSON
                import json
                ruta = f"datos/{archivo}"
                with open(ruta, "r", encoding="utf-8") as f:
                    datos_existentes = json.load(f)
                datos_existentes.append(nueva_entrada)
                with open(ruta, "w", encoding="utf-8") as f:
                    json.dump(datos_existentes, f, ensure_ascii=False, indent=2)

                print("✅ ¡Gracias! Tu aporte fue guardado para mejorar el asistente.")
                return nueva_respuesta

            elif opcion in ["1", "2", "3"]:
                i = int(opcion) - 1
                if i < len(sugerencias):
                    return sugerencias[i][2]  # respuesta asociada a la sugerencia elegida

            # Si la opción no es válida, avisa y vuelve a preguntar
            print(idi["opcion_invalida"])

    else:
        # 6. Si no hay ni coincidencias ni sugerencias, devuelve un mensaje por defecto
        return f"{idi['respuesta_default']}"


def iniciar_asistente():
    """
    Inicia el asistente conversacional interactivo.

    Permite al usuario seleccionar un idioma y personaje, y luego mantener un diálogo
    con el asistente. El sistema puede responder preguntas, calcular promedios,
    mostrar ayuda o aprender nuevas respuestas. El bucle continúa hasta que el usuario
    indique que quiere salir.

    No recibe parámetros.
    No retorna nada.
    """

    # 1. Elección de idioma e inicialización de textos
    idioma = elegir_idioma()
    idi = IDIOMAS[idioma]
    print(idi["bienvenida"])

    # 2. Elección de personaje (Nala, Luigi u Otto)
    nombre = elegir_personaje(idi)
    print(f"{idi['elegiste']} {nombre.capitalize()} 🐾\n")

    # 3. Cargar preguntas/respuestas desde el archivo correspondiente
    archivo = ARCHIVOS[idioma][nombre]
    datos = leer_json(f"datos/{archivo}")

    # 4. Cargar el stemmer para el idioma actual
    stemmer = stemmer_por_idioma(idioma)

    # 5. Bucle principal de conversación
    while True:
        print(f"\n{idi['consulta']}")
        consulta = input("> ").strip()

        # 6. Verificar si el usuario quiere salir
        if consulta.lower() in SALIDAS_VALIDAS:
            # NOTA: idi["despedida"] no existe, por eso se usa solo hasta_pronto
            print(idi["hasta_pronto"])
            break

        # 7. Verificar si el usuario quiere calcular promedio
        if contiene_palabra_clave(consulta, PALABRAS_PROMEDIO):
            promedio = calcular_promedio(idi)
            print(f"{idi['promedio_final']} {promedio:.2f}")
            registrar_log(nombre, idioma, consulta, promedio)

        # 8. Verificar si el usuario pidió ayuda
        elif contiene_palabra_clave(consulta, PALABRAS_AYUDA):
            print(idi["mensaje_ayuda"])

        # 9. Si no es salida, ni promedio ni ayuda: buscar respuesta normal
        else:
            respuesta = obtener_respuesta(consulta, datos, nombre, stemmer, idioma, idi, archivo)
            intro = random.choice(idi["respuestas_personaje"][nombre])
            print(f"{intro} {respuesta}")
            registrar_log(nombre, idioma, consulta, respuesta)