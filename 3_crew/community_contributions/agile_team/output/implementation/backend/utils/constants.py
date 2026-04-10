"""
Constantes del sistema utilizadas en toda la aplicación.
"""

# =============================================================================
# CONSTANTES DE TIEMPO
# =============================================================================

MONTH_NAMES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

MONTH_NAMES_SHORT = [
    "Ene", "Feb", "Mar", "Abr", "May", "Jun",
    "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
]

# =============================================================================
# CONSTANTES DE VALIDACIÓN
# =============================================================================

MIN_USERNAME_LENGTH = 4
MIN_PASSWORD_LENGTH = 4
MIN_FULLNAME_LENGTH = 3
MAX_DESCRIPTION_LENGTH = 200
MIN_AMOUNT = 0.01
MAX_AMOUNT = 999999999.99

# =============================================================================
# CONSTANTES DE CATEGORÍAS
# =============================================================================

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

# =============================================================================
# CONSTANTES DE MENSAJES
# =============================================================================

MSG_LOGIN_SUCCESS = "¡Bienvenido {name}! Has iniciado sesión correctamente."
MSG_LOGIN_ERROR = "Credenciales inválidas. Verifica tu usuario y contraseña."
MSG_REGISTER_SUCCESS = "¡Cuenta creada exitosamente! Ya puedes iniciar sesión."
MSG_REGISTER_ERROR = "No se pudo crear la cuenta. El usuario ya existe."
MSG_EXPENSE_CREATED = "Gasto registrado exitosamente."
MSG_EXPENSE_UPDATED = "Gasto actualizado exitosamente."
MSG_EXPENSE_DELETED = "Gasto eliminado exitosamente."
MSG_LOGOUT_SUCCESS = "Sesión cerrada correctamente."

ERR_USERNAME_TOO_SHORT = "El nombre de usuario debe tener al menos 4 caracteres"
ERR_PASSWORD_TOO_SHORT = "La contraseña debe tener al menos 4 caracteres"
ERR_FULLNAME_TOO_SHORT = "El nombre completo debe tener al menos 3 caracteres"
ERR_USERNAME_EXISTS = "El nombre de usuario ya está en uso"
ERR_USER_NOT_FOUND = "El usuario no existe"
ERR_WRONG_PASSWORD = "Contraseña incorrecta"
ERR_AMOUNT_REQUIRED = "El monto es obligatorio y debe ser mayor a 0"
ERR_AMOUNT_POSITIVE = "El monto debe ser un valor positivo"
ERR_DESCRIPTION_TOO_LONG = "La descripción no puede exceder 200 caracteres"
ERR_DATE_FUTURE = "La fecha no puede ser futura"
ERR_DATE_REQUIRED = "La fecha es obligatoria"
ERR_USER_NOT_AUTHENTICATED = "Debes iniciar sesión para realizar esta acción"
ERR_EXPENSE_NOT_FOUND = "El gasto no fue encontrado"
ERR_UNAUTHORIZED = "No tienes permiso para realizar esta acción"

MSG_NO_EXPENSES = "No tienes gastos registrados. ¡Comienza añadiendo tu primer gasto!"
MSG_NO_EXPENSES_PERIOD = "No hay gastos registrados para el período seleccionado."

# =============================================================================
# CONSTANTES DE CONFIGURACIÓN DE APLICACIÓN
# =============================================================================

DEFAULT_APP_TITLE = "Gestor de Gastos Personales"
DEFAULT_APP_DESCRIPTION = "Aplicación para gestionar tus gastos personales de forma inteligente"
DEFAULT_SERVER_PORT = 7860
DEFAULT_SERVER_HOST = "0.0.0.0"
