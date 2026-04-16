from traders import Trader
from typing import List
import asyncio
from tracers import LogTracer
from agents import add_trace_processor
from market import is_market_open
from dotenv import load_dotenv
import os

load_dotenv(override=True)

RUN_EVERY_N_MINUTES = int(os.getenv("RUN_EVERY_N_MINUTES", "60"))
RUN_EVEN_WHEN_MARKET_IS_CLOSED = (
    os.getenv("RUN_EVEN_WHEN_MARKET_IS_CLOSED", "true").strip().lower() == "true"
)
USE_MANY_MODELS = os.getenv("USE_MANY_MODELS", "true").strip().lower() == "true"

names = ["Warren", "George", "Ray", "Cathie"]
lastnames = ["Patience", "Bold", "Systematic", "Crypto"]

print(f"Configuración: Ejecutar cada {RUN_EVERY_N_MINUTES} minutos, incluso si el mercado está cerrado: {RUN_EVEN_WHEN_MARKET_IS_CLOSED}, usar muchos modelos: {USE_MANY_MODELS}")

if USE_MANY_MODELS:
    model_names = [
        "gpt-4.1-mini",
        "mistral-large-3:675b",
        "kimi-k2.5",
        "llama-3.3-70b-versatile",
    ]
    short_model_names = ["GPT 4.1 Mini", "Mistra Large", "Gemini 2.0 Flash", "Llama 3.3 Versatile"]
else:
    model_names = ["gpt-4o-mini"] * 4
    short_model_names = ["GPT 4o mini"] * 4


def create_traders() -> List[Trader]:
    traders = []
    for name, lastname, model_name in zip(names, lastnames, model_names):
        print(f"Creando trader {name} {lastname} con modelo {model_name}")
        traders.append(Trader(name, lastname, model_name))
    return traders


async def run_every_n_minutes():
    add_trace_processor(LogTracer())
    traders = create_traders()
    while True:
        if RUN_EVEN_WHEN_MARKET_IS_CLOSED or is_market_open():
            await asyncio.gather(*[trader.run() for trader in traders])
        else:
            print("El mercado está cerrado, no lo vamos a ejecutar.")
        await asyncio.sleep(RUN_EVERY_N_MINUTES * 60)


if __name__ == "__main__":
    print(f"Iniciando el programador para ejecutarse cada {RUN_EVERY_N_MINUTES} minutos")
    asyncio.run(run_every_n_minutes())
