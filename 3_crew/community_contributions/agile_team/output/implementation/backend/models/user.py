"""
Modelo de Usuario.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    """Entidad que representa un usuario del sistema."""
    username: str
    password: str
    full_name: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    
    def __post_init__(self):
        if len(self.username) < 4:
            raise ValueError("El nombre de usuario debe tener al menos 4 caracteres")
        if len(self.password) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres")
        if len(self.full_name) < 3:
            raise ValueError("El nombre completo debe tener al menos 3 caracteres")
