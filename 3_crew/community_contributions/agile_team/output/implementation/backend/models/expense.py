"""
Modelo de Gasto.
"""

from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Expense:
    """Entidad que representa un gasto registrado por un usuario."""
    user_id: str
    description: str
    amount: float
    date: datetime
    category: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        if len(self.description) > 200:
            raise ValueError("La descripción no puede exceder 200 caracteres")
        if self.date > datetime.now():
            raise ValueError("La fecha no puede ser futura")

    def update(self, description: str = None, amount: float = None,
               date: datetime = None, category: str = None):
        """Actualiza los campos del gasto."""
        if description is not None:
            if len(description) > 200:
                raise ValueError("La descripción no puede exceder 200 caracteres")
            self.description = description
        if amount is not None:
            if amount <= 0:
                raise ValueError("El monto debe ser mayor a cero")
            self.amount = amount
        if date is not None:
            if date > datetime.now():
                raise ValueError("La fecha no puede ser futura")
            self.date = date
        if category is not None:
            self.category = category
        self.updated_at = datetime.now()
