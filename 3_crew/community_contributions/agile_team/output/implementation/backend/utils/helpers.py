"""
Funciones auxiliares utilitarias.

Este módulo proporciona funciones auxiliares utilizadas
en diferentes partes de la aplicación.
"""

import uuid
from datetime import datetime
from calendar import monthrange
from typing import Optional

MONTH_NAMES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

MONTH_NAMES_SHORT = [
    "Ene", "Feb", "Mar", "Abr", "May", "Jun",
    "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
]


def generate_id() -> str:
    """Genera un identificador único usando UUID."""
    return str(uuid.uuid4())


def format_currency(amount: float, currency_symbol: str = "$") -> str:
    """Formatea un monto como cadena de moneda."""
    return f"{currency_symbol}{amount:,.2f}"


def format_date(date: datetime, format_str: str = "%d/%m/%Y") -> str:
    """Formatea una fecha como cadena."""
    return date.strftime(format_str)


def get_month_name(month: int, short: bool = False) -> str:
    """Obtiene el nombre de un mes según su número."""
    names = MONTH_NAMES_SHORT if short else MONTH_NAMES
    if 1 <= month <= 12:
        return names[month - 1]
    return ""


def get_month_number(month_name: str) -> int:
    """Obtiene el número de un mes según su nombre."""
    for i, name in enumerate(MONTH_NAMES, start=1):
        if name.lower() == month_name.lower():
            return i
    for i, name in enumerate(MONTH_NAMES_SHORT, start=1):
        if name.lower() == month_name.lower():
            return i
    return 0


def get_days_in_month(year: int, month: int) -> int:
    """Obtiene el número de días en un mes específico."""
    return monthrange(year, month)[1]


def get_date_range(year: int, month: int) -> tuple:
    """Obtiene el rango de fechas (inicio y fin) de un mes."""
    days = get_days_in_month(year, month)
    start = datetime(year, month, 1, 0, 0, 0)
    end = datetime(year, month, days, 23, 59, 59)
    return start, end


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    """Parsea una cadena de fecha a datetime."""
    try:
        return datetime.strptime(date_str, format_str)
    except (ValueError, TypeError):
        return None


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """Trunca una cadena si excede la longitud máxima."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def calculate_percentage(part: float, total: float) -> float:
    """Calcula el porcentaje de una parte respecto al total."""
    if total == 0:
        return 0.0
    return (part / total) * 100


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Realiza una división segura que maneja división por cero."""
    if denominator == 0:
        return default
    return numerator / denominator


def get_current_period() -> tuple:
    """Obtiene el período actual (año y mes)."""
    now = datetime.now()
    return now.year, now.month


def is_same_period(date: datetime, year: int, month: int) -> bool:
    """Verifica si una fecha pertenece a un período específico."""
    return date.year == year and date.month == month
