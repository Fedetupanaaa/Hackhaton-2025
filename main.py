import discord
import requests
from discord.ext import commands
import pyttsx3
from deep_translator import GoogleTranslator
import random


def traducir(text: str) -> str:
    """Traduce de inglés a español."""
    try:
        return GoogleTranslator(source="en", target="es").translate(text)
    except Exception as e:
        print("Error al traducir:", e)
        return text


def talk(text: str):
    """Lee en voz alta un texto con pyttsx3."""
    engine = pyttsx3.init()
    engine.setProperty("rate", 125)
    engine.setProperty("volume", 1.0)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.say(text)
    engine.runAndWait()


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.command()
async def hola(ctx):
    await ctx.send("Hola soy tu asistente virtual")
    talk("Hola soy tu asistente virtual")


def climate_datazo() -> str:
    endpoints = [
        ("temp global", "https://global-warming.org/api/temperature-api"),
        ("CO₂ atmosférico", "https://global-warming.org/api/co2-api"),
        ("metano atmosférico", "https://global-warming.org/api/methane-api"),
    ]
    etiqueta, url = random.choice(endpoints)
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        if etiqueta == "temp global":
            lista = data.get("result", [])
            if not lista:
                return "No se encontraron datos de temperatura."
            ultimo = lista[-1]
            year = ultimo.get("year") or ultimo.get("time") or "desconocido"
            valor = ultimo.get("station") or ultimo.get("land") or "?"
            return f"Dato climático — {etiqueta}: {valor} °C en {year}."
        elif etiqueta == "CO₂ atmosférico":
            lista = data.get("co2", [])
            if not lista:
                return "No se encontraron datos de CO₂."
            ultimo = lista[-1]
            year = ultimo.get("year") or ultimo.get("date") or "desconocido"
            valor = ultimo.get("trend", "?")
            return f"Dato climático — {etiqueta}: {valor} ppm en {year}."
        elif etiqueta == "metano atmosférico":
            lista = data.get("methane", [])
            if not lista:
                return "No se encontraron datos de metano."
            ultimo = lista[-1]
            year = ultimo.get("year") or ultimo.get("date") or "desconocido"
            valor = ultimo.get("trend", "?")
            return f"Dato climático — {etiqueta}: {valor} ppb en {year}."
        else:
            return "No se pudo interpretar el dato recibido"
    else:
        return "Error: no se pudo conectar a la API"


"""Comando para obtener dato curioso
sobre clima."""


@bot.command()
async def infoatmosfera(ctx):
    factu = climate_datazo()
    await ctx.send(f"Tu dato curioso atmosférico es: {factu}")


# Preguntas del cuestionario de huella de carbono
preguntas = [
    {
        "pregunta": "🚗 ¿Con qué frecuencia usas el automóvil?",
        "opciones": [
            "A) Nunca",
            "B) A veces",
            "C) Todos los días"
        ],
        "puntajes": {"A": 0, "B": 1, "C": 3}
    },
    {
        "pregunta": "♻️ ¿Sueles reciclar?",
        "opciones": [
            "A) Nunca",
            "B) De vez en cuando",
            "C) Todos los días"
        ],
        "puntajes": {"A": 4, "B": 2, "C": 0}
    },
    {
        "pregunta": "💡 ¿Cómo es tu consumo de electricidad?",
        "opciones": [
            "A) Uso energías renovables",
            "B) Consumo moderado",
            "C) Consumo alto"
        ],
        "puntajes": {"A": 0, "B": 2, "C": 4}
    },
    {
        "pregunta": "✈️ ¿Con qué frecuencia viajas en avión?",
        "opciones": [
            "A) Nunca",
            "B) 1-2 veces al año",
            "C) Varias veces al año"
        ],
        "puntajes": {"A": 0, "B": 3, "C": 6}
    },
    {
        "pregunta": "🚬 ¿Fumas con  frecuencia?",
        "opciones": [
            "A) Nunca",
            "B) de vez en cuando",
            "C) siempre"
        ],
        "puntajes": {"A": 0, "B": 2, "C": 3}
    },
    {
        "pregunta": "👕 ¿Cada cuánto compras ropa nueva?",
        "opciones": [
            "A) Muy poco (1–2 veces al año)",
            "B) Regular (cada 2–3 meses)",
            "C) Muy seguido (casi todos los meses)"
        ],
        "puntajes": {"A": 0, "B": 2, "C": 3}
    }

]

"""Comando para iniciar cuestionario
de huella de carbono."""


@bot.command()
async def huella(ctx):
    score = 0
    await ctx.send(
        " ¡Vamos a calcular tu huella de carbono! "
        "Responde con A, B o C."
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    for p in preguntas:
        opciones_texto = "\n".join(p["opciones"])
        await ctx.send(f" {p['pregunta']}\n{opciones_texto}")
        try:
            msg = await bot.wait_for(
                "message", timeout=25.0, check=check
            )
            respuesta = msg.content.upper()
            if respuesta in p["puntajes"]:
                puntos = p["puntajes"][respuesta]
                score += puntos
                await ctx.send(
                    f" Respuesta registrada (+{puntos} puntos de CO₂)"
                )
            else:
                await ctx.send(" Responde solo con A, B o C.")
        except Exception:
            await ctx.send(" Tiempo agotado para esta pregunta.")
    if score <= 5:
        resultado = " Tu huella de carbono es baja. Bien hecho!"
    elif score <= 10:
        resultado = (
            " Tu huella de carbono es media. "
            "Se puede mejorar."
        )
    else:
        resultado = (
            " Tu huella de carbono es **alta**. "
            "Intenta reducir tus emisiones."
        )
    await ctx.send(
        f"terminado\n"
        f"Puntuación total: {score}\n"
        f"{resultado}"
    )


bot.run(
    "Tu_Token_Aqui"
)
