"""
Módulo de configuración de categorías.
"""

CATEGORY_NAMES = [
    "Vivienda",
    "Alimentación",
    "Transporte",
    "Entretenimiento",
    "Compras",
    "Salud",
    "Educación",
    "Otros"
]

CATEGORY_ICONS = {
    "Vivienda": "🏠",
    "Alimentación": "🍔",
    "Transporte": "🚗",
    "Entretenimiento": "🎮",
    "Compras": "🛒",
    "Salud": "💊",
    "Educación": "📚",
    "Otros": "💰",
}

CATEGORY_COLORS = {
    "Vivienda": "#2E86AB",
    "Alimentación": "#A23B72",
    "Transporte": "#F18F01",
    "Entretenimiento": "#C73E1D",
    "Compras": "#3B1F2B",
    "Salud": "#95C11F",
    "Educación": "#7B2D8E",
    "Otros": "#6B7280",
}

CATEGORY_KEYWORDS = {
    "Vivienda": [
        "alquiler", "hipoteca", "luz", "agua", "gas", "internet", 
        "teléfono", "mantenimiento", "reforma", "muebles", "renta",
        "servicios", "electricidad", "fibra", "cable"
    ],
    "Alimentación": [
        "comida", "supermercado", "restaurante", "cena", "almuerzo", 
        "desayuno", "fruta", "verdura", "carne", "pescado", "pan", 
        "leche", "cafe", "delivery", "外卖", "vianda", "gastos"
    ],
    "Transporte": [
        "gasolina", "diesel", "taxi", "uber", "bus", "metro", 
        "tren", "estacionamiento", "peaje", "mantenimiento coche",
        "neumáticos", "seguro coche", "combustible", "pasaje"
    ],
    "Entretenimiento": [
        "cine", "netflix", "spotify", "amazon prime", "videojuego", 
        "juego", "concierto", "teatro", "museo", "excursión", 
        "viaje", "vacaciones", "streaming", "hbo", "disney"
    ],
    "Compras": [
        "ropa", "zapatos", "electrónica", "teléfono", "computadora", 
        "tablet", "hogar", "decoración", "regalo", "amazon", 
        "tienda", "compras", "market", "boutique", "moda"
    ],
    "Salud": [
        "médico", "farmacia", "medicina", "doctor", "dentista", 
        "psicólogo", "gimnasio", "fitness", "yoga", "deporte", 
        "seguro médico", "hospital", "clínica", "tratamiento"
    ],
    "Educación": [
        "curso", "universidad", "libro", "escuela", "formación", 
        "certificación", "suscripción", "revista", "periodico", 
        "audiolibro", "educación", "estudio", "colegio", "tesis"
    ],
    "Otros": []
}

__all__ = [
    'CATEGORY_NAMES',
    'CATEGORY_ICONS',
    'CATEGORY_COLORS',
    'CATEGORY_KEYWORDS'
]
