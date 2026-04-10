"""
Servicio de Autenticación.
"""

from typing import Optional

from models.user import User
from models.base import Result
from repositories.user_repository import UserRepository


class AuthService:
    """Servicio de autenticación que maneja registro, login y logout de usuarios."""
    
    def __init__(self, user_repository: UserRepository):
        self._repository = user_repository
        self._current_user: Optional[User] = None
    
    def register(self, username: str, password: str, full_name: str) -> Result:
        """Registra un nuevo usuario en el sistema."""
        if len(username) < 4:
            return Result.fail("El nombre de usuario debe tener al menos 4 caracteres")
        if len(password) < 4:
            return Result.fail("La contraseña debe tener al menos 4 caracteres")
        if len(full_name) < 3:
            return Result.fail("El nombre completo debe tener al menos 3 caracteres")
        
        if self._repository.exists(username):
            return Result.fail("El nombre de usuario ya está en uso", "USERNAME_EXISTS")
        
        try:
            user = User(username=username, password=password, full_name=full_name)
            self._repository.add(user)
            return Result.ok(user)
        except ValueError as e:
            return Result.fail(str(e))
    
    def login(self, username: str, password: str) -> Result:
        """Autentica a un usuario con sus credenciales."""
        if not username or not password:
            return Result.fail("El usuario y la contraseña son requeridos")
        
        user = self._repository.get_by_username(username)
        
        if user is None:
            return Result.fail("El usuario no existe", "USER_NOT_FOUND")
        
        if not user.is_active:
            return Result.fail("La cuenta está desactivada", "ACCOUNT_INACTIVE")
        
        if user.password != password:
            return Result.fail("Contraseña incorrecta", "WRONG_PASSWORD")
        
        self._current_user = user
        return Result.ok(user)
    
    def logout(self) -> None:
        """Cierra la sesión del usuario actual."""
        self._current_user = None
    
    def get_current_user(self) -> Optional[User]:
        """Obtiene el usuario actualmente autenticado."""
        return self._current_user
    
    def is_authenticated(self) -> bool:
        """Verifica si hay un usuario autenticado en la sesión."""
        return self._current_user is not None
    
    def get_current_user_id(self) -> Optional[str]:
        """Obtiene el ID del usuario autenticado."""
        return self._current_user.username if self._current_user else None
    
    def get_current_user_name(self) -> Optional[str]:
        """Obtiene el nombre completo del usuario autenticado."""
        return self._current_user.full_name if self._current_user else None
