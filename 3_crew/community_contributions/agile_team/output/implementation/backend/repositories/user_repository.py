"""
Repositorio de Usuarios.
"""

from typing import Dict, List, Optional

from models.user import User


class UserRepository:
    """Repositorio para gestionar usuarios en memoria."""
    
    def __init__(self):
        self._storage: Dict[str, User] = {}
    
    def add(self, user: User) -> User:
        if user.username in self._storage:
            raise ValueError(f"El usuario '{user.username}' ya existe")
        self._storage[user.username] = user
        return user
    
    def update(self, user: User) -> Optional[User]:
        if user.username not in self._storage:
            return None
        self._storage[user.username] = user
        return user
    
    def delete(self, username: str) -> bool:
        if username in self._storage:
            del self._storage[username]
            return True
        return False
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self._storage.get(username)
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._storage.get(user_id)
    
    def get_all(self) -> List[User]:
        return list(self._storage.values())
    
    def exists(self, username: str) -> bool:
        return username in self._storage
    
    def get_active_users(self) -> List[User]:
        return [user for user in self._storage.values() if user.is_active]
    
    def count(self) -> int:
        return len(self._storage)
    
    def clear(self) -> None:
        self._storage.clear()
