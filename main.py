import discord
import requests
from discord.ext import commands
from deep_translator import GoogleTranslator
import random


def traducir(text: str) -> str:
    """Traduce de inglés a español."""
    try:
        return GoogleTranslator(source="en", target="es").translate(text)
    except Exception as e:
        print("Error al traducir:", e)
        return text


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

"""Comando para definir cambio climático."""


@bot.command()
async def cambioclimatico(ctx):
    await ctx.send("cambio previsible en el clima terrestre"
                   " provocado por la acción humana"
                   " que da lugar al efecto invernadero"
                   " y al calentamiento global")

"""Comando de ayuda."""


@bot.command()
async def Recomendaciones(ctx):
    await ctx.send(f"Una recomendacion {random.choice(consejomedia)}"
                   f"o este {random.choice(consejoalta)}")


@bot.command()
async def ayuda(ctx):
    await ctx.send(" puede utilizar el comando $infoatmosfera"
                   " para obtener información sobre la atmósfera"
                   " y su relación con el cambio climático"
                   ". También puede usar el comando $huella "
                   "para iniciar un cuestionario sobre la huella de carbono"
                   " y saber si es baja, media o alta."
                   "tambien puede utilizar el comando $cambioclimatico"
                   "Para saber que es el cambio climatico"
                   "el comando $datocurioso"
                   " para obtener un dato curioso sobre el clima."
                   "Finalmente, el comando $Recomendaciones para obtener "
                   "obviamente recomendaciones")

consejomedia = [
    "usar transporte público en lugar de conducir",
    "compartir coche con otras personas",
    "caminar o andar en bicicleta para distancias cortas",
    "reducir el uso de aire acondicionado",
    "apagar las luces y  dispositivos electrónicos cuando no se usan"
]
consejoalta = [
    "Usar bombillas de bajo consumo o LED",
    "instalar paneles solares en casa",
    "Utilizar electrodomésticos que utilizen bajo consumo de energía",
    "reducir el consumo de carne y productos lácteos",
    "Comprar productos locales y de temporada"
]

"""Función para obtener informacion de la atmosfera"""


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


"""Preguntas del cuestionario de huella de carbono"""

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
            f"por que no pruebas con {random.choice(consejomedia)}"
        )
    else:
        resultado = (
            " Tu huella de carbono es alta. "
            "Intenta reducir tus emisiones."
            f"por que no pruebas con {random.choice(consejoalta)}"
        )
    await ctx.send(
        f"terminado\n"
        f"Puntuación total: {score}\n"
        f"{resultado}"
    )

"""Lista de datos curiosos sobre el clima."""

datocuriosos = [
    (
        "el dióxido de carbono (CO₂) es un gas de efecto invernadero "
        "que contribuye al calentamiento global"
    ),
    (
        "el metano (CH₄) es otro gas de efecto invernadero, con un "
        "potencial de calentamiento mucho mayor que el CO₂"
    ),
    (
        "la deforestación libera grandes cantidades de CO₂ a la atmósfera "
        "y reduce la capacidad de los bosques para absorberlo"
    ),
    (
        "los océanos absorben aproximadamente el 30% del CO₂ emitido por "
        "las actividades humanas, lo que provoca la acidificación del agua"
    ),
    (
        "el uso de energías renovables, como la solar y la eólica, puede "
        "reducir significativamente las emisiones de gases de efecto "
        "invernadero"
    ),
    (
        "el transporte es una de las principales fuentes de emisiones de "
        "CO₂ a nivel mundial"
    ),
    (
        "la agricultura intensiva contribuye a las emisiones de metano y "
        "óxido nitroso, ambos gases de efecto invernadero potentes"
    ),
    (
        "el aumento de la temperatura global está provocando el derretimiento "
        "de los glaciares y el aumento del nivel del mar"
    ),
    (
        "las ciudades suelen tener temperaturas más altas que las zonas "
        "rurales debido al efecto isla de calor urbano"
    ),
    (
        "la contaminación del aire no solo afecta la salud humana, sino que "
        "también puede influir en el clima local y global"
    ),
]

"""Comando para datos curiosos del clima."""


@bot.command()
async def datocurioso(ctx):
    datocuro = random.choice(datocuriosos)
    await ctx.send(f"Hay te va un dato curioso: {datocuro}")


bot.run(
    "Tu_Token_Aqui"
)
