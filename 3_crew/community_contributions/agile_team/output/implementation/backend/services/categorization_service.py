"""
Servicio de Categorización.
"""

from typing import List, Optional

from models.category import Category
from repositories.category_repository import CategoryRepository


class CategorizationService:
    """Servicio de categorización automática de gastos."""
    
    DEFAULT_CATEGORY = "Otros"
    
    def __init__(self, category_repository: CategoryRepository):
        self._repository = category_repository
    
    def categorize(self, description: str) -> Category:
        """Categoriza automáticamente un gasto basado en su descripción."""
        if not description:
            return self._repository.get_by_name(self.DEFAULT_CATEGORY) or Category(name="Otros")
        
        text_lower = description.lower()
        
        for category in self._repository.get_all():
            if category.name == self.DEFAULT_CATEGORY:
                continue
            
            for keyword in category.keywords:
                if keyword.lower() in text_lower:
                    return category
        
        return self._repository.get_by_name(self.DEFAULT_CATEGORY) or Category(name="Otros")
    
    def get_all_categories(self) -> List[Category]:
        """Obtiene todas las categorías disponibles."""
        return self._repository.get_all()
    
    def get_category_names(self) -> List[str]:
        """Obtiene solo los nombres de las categorías disponibles."""
        return self._repository.get_names()
    
    def get_category_by_name(self, name: str) -> Optional[Category]:
        """Obtiene una categoría específica por su nombre."""
        return self._repository.get_by_name(name)
    
    def get_category_with_icon(self, category_name: str) -> str:
        """Obtiene el nombre de la categoría con su icono."""
        category = self._repository.get_by_name(category_name)
        if category:
            return f"{category.icon} {category.name}"
        return f"💰 {category_name}"
