"""
Funciones de validación para los datos de la aplicación.
"""

from datetime import datetime
from typing import Optional, Tuple

MIN_USERNAME_LENGTH = 4
MIN_PASSWORD_LENGTH = 4
MIN_FULLNAME_LENGTH = 3
MAX_DESCRIPTION_LENGTH = 200
MIN_AMOUNT = 0.01


class ValidationError(Exception):
    """Excepción personalizada para errores de validación."""
    
    def __init__(self, message: str, field: Optional[str] = None, code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.field = field
        self.code = code
    
    def __str__(self) -> str:
        if self.field:
            return f"{self.field}: {self.message}"
        return self.message


def validate_username(username: str) -> Tuple[bool, Optional[str]]:
    """Valida el nombre de usuario."""
    if not username:
        return False, "El nombre de usuario es obligatorio"
    if len(username) < MIN_USERNAME_LENGTH:
        return False, f"El nombre de usuario debe tener al menos {MIN_USERNAME_LENGTH} caracteres"
    if not username.isalnum():
        return False, "El nombre de usuario debe contener solo letras y números"
    return True, None


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """Valida la contraseña."""
    if not password:
        return False, "La contraseña es obligatoria"
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres"
    return True, None


def validate_full_name(full_name: str) -> Tuple[bool, Optional[str]]:
    """Valida el nombre completo del usuario."""
    if not full_name:
        return False, "El nombre completo es obligatorio"
    if len(full_name) < MIN_FULLNAME_LENGTH:
        return False, f"El nombre completo debe tener al menos {MIN_FULLNAME_LENGTH} caracteres"
    return True, None


def validate_amount(amount: Optional[float]) -> Tuple[bool, Optional[str]]:
    """Valida el monto de un gasto."""
    if amount is None:
        return False, "El monto es obligatorio y debe ser mayor a 0"
    try:
        amount_float = float(amount)
    except (ValueError, TypeError):
        return False, "El monto debe ser un valor numérico válido"
    if amount_float <= 0:
        return False, "El monto debe ser un valor positivo"
    if amount_float < MIN_AMOUNT:
        return False, "El monto debe ser mayor o igual a 0.01"
    return True, None


def validate_description(description: Optional[str]) -> Tuple[bool, Optional[str]]:
    """Valida la descripción de un gasto."""
    if description is None:
        return True, None
    if len(description) > MAX_DESCRIPTION_LENGTH:
        return False, f"La descripción no puede exceder {MAX_DESCRIPTION_LENGTH} caracteres"
    return True, None


def validate_date(date: Optional[datetime]) -> Tuple[bool, Optional[str]]:
    """Valida la fecha de un gasto."""
    if date is None:
        return False, "La fecha es obligatoria"
    if date > datetime.now():
        return False, "La fecha no puede ser futura"
    return True, None


def validate_expense_data(
    description: Optional[str],
    amount: Optional[float],
    date: Optional[datetime],
    category: Optional[str] = None
) -> Tuple[bool, list]:
    """Valida todos los campos de un gasto."""
    errors = []
    
    is_valid, error = validate_amount(amount)
    if not is_valid:
        errors.append(error)
    
    is_valid, error = validate_description(description)
    if not is_valid:
        errors.append(error)
    
    is_valid, error = validate_date(date)
    if not is_valid:
        errors.append(error)
    
    if category is not None:
        CATEGORY_NAMES = ["Vivienda", "Alimentación", "Transporte", "Entretenimiento", 
                         "Compras", "Salud", "Educación", "Otros"]
        if category not in CATEGORY_NAMES:
            errors.append(f"La categoría '{category}' no es válida")
    
    return len(errors) == 0, errors


def validate_auth_data(
    username: str,
    password: str,
    full_name: Optional[str] = None
) -> Tuple[bool, list]:
    """Valida los datos de autenticación."""
    errors = []
    
    is_valid, error = validate_username(username)
    if not is_valid:
        errors.append(error)
    
    is_valid, error = validate_password(password)
    if not is_valid:
        errors.append(error)
    
    if full_name is not None:
        is_valid, error = validate_full_name(full_name)
        if not is_valid:
            errors.append(error)
    
    return len(errors) == 0, errors
