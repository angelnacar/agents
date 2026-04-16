from polygon import ReferenceClient, StocksClient
from dotenv import load_dotenv
import os
from datetime import datetime
import random
from database import write_market, read_market
from functools import lru_cache
from datetime import timezone

load_dotenv(override=True)

polygon_api_key = os.getenv("POLYGON_API_KEY")
polygon_plan = os.getenv("POLYGON_PLAN")

is_paid_polygon = polygon_plan == "paid"
is_realtime_polygon = polygon_plan == "realtime"


def is_market_open() -> bool:
    client = ReferenceClient(polygon_api_key)
    market_status = client.get_market_status()
    return market_status.get("market") == "open"


def get_all_share_prices_polygon_eod() -> dict[str, float]:
    """Con mucho agradecimiento a la estudiante Reema R. por arreglar el problema de la zona horaria en esto!"""
    client = StocksClient(polygon_api_key)

    probe_response = client.get_previous_close("SPY")
    probe_results = probe_response.get("results", []) if isinstance(probe_response, dict) else []
    if not probe_results:
        return {}

    probe = probe_results[0]
    last_close = datetime.fromtimestamp(probe.get("t", 0) / 1000, tz=timezone.utc).date()

    bars_response = client.get_grouped_daily_bars(last_close, adjusted=True)
    return {
        result.get("T"): result.get("c", 0.0)
        for result in bars_response.get("results", [])
        if result.get("T")
    }


@lru_cache(maxsize=2)
def get_market_for_prior_date(today):
    market_data = read_market(today)
    if not market_data:
        market_data = get_all_share_prices_polygon_eod()
        write_market(today, market_data)
    return market_data


def get_share_price_polygon_eod(symbol) -> float:
    today = datetime.now().date().strftime("%Y-%m-%d")
    market_data = get_market_for_prior_date(today)
    return market_data.get(symbol, 0.0)


def get_share_price_polygon_min(symbol) -> float:
    client = StocksClient(polygon_api_key)
    result = client.get_snapshot(symbol)
    if not isinstance(result, dict):
        return 0.0

    min_close = result.get("min", {}).get("c")
    prev_close = result.get("prevDay", {}).get("c")
    return float(min_close or prev_close or 0.0)


def get_share_price_polygon(symbol) -> float:
    if is_paid_polygon:
        return get_share_price_polygon_min(symbol)
    else:
        return get_share_price_polygon_eod(symbol)


def get_share_price(symbol) -> float:
    if polygon_api_key:
        try:
            return get_share_price_polygon(symbol)
        except Exception as e:
            print(f"No se pudo usar la API de Polygon debido a {e}; usando un número aleatorio")
    return float(random.randint(1, 100))
