"""
Clase base Result para manejo de operaciones.
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Result:
    """Tipo Result para manejo de errores sin excepciones."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    
    @classmethod
    def ok(cls, data: Any = None) -> 'Result':
        """Crea un resultado exitoso."""
        return cls(success=True, data=data)
    
    @classmethod
    def fail(cls, error: str, error_code: str = None) -> 'Result':
        """Crea un resultado de error."""
        return cls(success=False, error=error, error_code=error_code)
    
    @property
    def is_success(self) -> bool:
        return self.success
    
    @property
    def is_failure(self) -> bool:
        return not self.success
