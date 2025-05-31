from nltk.stem.snowball import SnowballStemmer

IDIOMAS = {
    "es": {
        "bienvenida": "🐾 ¡Bienvenido al Miausistente!",
        "elige_opcion": "Elegí el personaje felino que te acompañará",
        "opciones_gatos": "1) Nala 🐱\n2) Luigi 🐈‍⬛\n3) Otto 🐾",
        "opcion_invalida": "Opción inválida. Probá de nuevo.",
        "elegiste": "Elegiste a",
        "consulta": "¿Sobre qué tema querés preguntar?",
        "consulta_continuar": "Decile algo a {nombre}!!",
        "respuesta_default": "No encontré una respuesta exacta, pero esto podría ayudarte:",
        "frases_no_se": [
            "Mmm... no encontré nada exacto.",
            "No estoy seguro de eso...",
            "Mi bigote detecta confusión, ¡pero tengo ideas!"
        ],
        "tal_vez_quisiste": "¿Tal vez quisiste preguntar por una de estas opciones?",
        "mensaje_ayuda": "Podés preguntarme sobre que hay en la UADE central, que tecnicaturas, licencuturas tenemos, etc... También puedo ayudarte a promediar tus notas.",
        "hasta_pronto": "¡Hasta pronto, humano! 🐾",
        "cuantos_parciales": "¿Cuántos parciales querés promediar?",
        "nota_parcial": "Nota del parcial",
        "tus_notas": "Estas son tus notas:",
        "despedida": "{nombre} se despide: {mensaje}",
        "promedio_final": "📊 Tu promedio final es:",
        "respuestas_personaje": {
            "nala": ["🐱 Nala dice:"],
            "luigi": ["🐈‍⬛ Luigi responde:"],
            "otto": ["🤖 Otto calcula:"]
        }
    },
    "en": {
        "bienvenida": "🐾 Welcome to the Meowssistant!",
        "elige_opcion": "Choose your feline assistant",
        "opciones_gatos": "1) Nala 🐱\n2) Luigi 🐈‍⬛\n3) Otto 🐾",
        "opcion_invalida": "Invalid option. Try again.",
        "despedida": "{nombre} says goodbye: {mensaje}",
        "elegiste": "You chose",
        "consulta": "What would you like to ask about?",
        "consulta_continuar": "Any more questions for {nombre}?",
        "respuesta_default": "I couldn’t find an exact match, but this might help:",
        "frases_no_se": [
            "Hmm... I couldn’t find anything exact.",
            "Not sure about that...",
            "My whiskers are tingling — maybe these help!"
        ],
        "tal_vez_quisiste": "Maybe you meant one of these:",
        "mensaje_ayuda": "You can ask me about what's available at UADE Central, what technical degrees and bachelor's programs we offer, etc... I can also help you calculate your grades.",
        "hasta_pronto": "See you next time, human! 🐾",
        "cuantos_parciales": "How many exams do you want to average?",
        "nota_parcial": "Grade",
        "tus_notas": "Here are your grades:",
        "promedio_final": "📊 Your final average is:",
        "respuestas_personaje": {
            "nala": ["🐱 Nala says:"],
            "luigi": ["🐈‍⬛ Luigi replies:"],
            "otto": ["🤖 Otto computes:"]
        }
    },
    "pt": {
        "bienvenida": "🐾 Bem-vindo ao Miaussistente!",
        "elige_opcion": "Escolha seu assistente felino",
        "opciones_gatos": "1) Nala 🐱\n2) Luigi 🐈‍⬛\n3) Otto 🐾",
        "opcion_invalida": "Opção inválida. Tente novamente.",
        "elegiste": "Você escolheu",
        "consulta": "Sobre o que você gostaria de perguntar?",
        "despedida": "{nombre} se despede: {mensaje}",
        "consulta_continuar": "Diga algo para {nombre}?",
        "respuesta_default": "Não encontrei uma resposta exata, mas isso pode te ajudar:",
        "frases_no_se": [
            "Hmm... não encontrei nada exato.",
            "Não tenho certeza disso...",
            "Minhas bigodes estão confusos — mas talvez isso ajude!"
        ],
        "tal_vez_quisiste": "Talvez você quis dizer:",
        "mensaje_ayuda": "Você pode me perguntar o que tem na UADE Central, quais cursos técnicos e graduações oferecemos, etc... Também posso te ajudar a calcular suas notas.",
        "hasta_pronto": "Até logo, humano! 🐾",
        "cuantos_parciales": "Quantas provas você quer calcular a média?",
        "nota_parcial": "Nota",
        "tus_notas": "Essas são suas notas:",
        "promedio_final": "📊 Sua média final é:",
        "respuestas_personaje": {
            "nala": ["🐱 Nala diz:"],
            "luigi": ["🐈‍⬛ Luigi responde:"],
            "otto": ["🤖 Otto calcula:"]
        }
    }
}

ARCHIVOS = {
    "es": {
        "nala": "espreguntasnala.json",
        "luigi": "espreguntasluigi.json",
        "otto": "espreguntasotto.json"
    },
    "en": {
        "nala": "enpreguntasnala.json",
        "luigi": "enpreguntasluigi.json",
        "otto": "enpreguntasotto.json"
    },
    "pt": {
        "nala": "ptpreguntasnala.json",
        "luigi": "ptpreguntasluigi.json",
        "otto": "ptpreguntasotto.json"
    }
}

def stemmer_por_idioma(idioma):
    return SnowballStemmer({
        "es": "spanish",
        "en": "english",
        "pt": "portuguese"
    }.get(idioma, "spanish"))
