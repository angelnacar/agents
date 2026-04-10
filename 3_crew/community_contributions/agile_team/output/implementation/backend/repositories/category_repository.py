"""
Repositorio de Categorías.
"""

from typing import List, Optional

from models.category import Category
from config.categories import CATEGORY_NAMES, CATEGORY_ICONS, CATEGORY_COLORS, CATEGORY_KEYWORDS


class CategoryRepository:
    """Repositorio para gestionar categorías de gastos."""
    
    def __init__(self):
        self._categories = self._load_categories()
    
    def _load_categories(self) -> List[Category]:
        return [
            Category(
                name=name,
                icon=CATEGORY_ICONS[name],
                keywords=CATEGORY_KEYWORDS[name],
                color=CATEGORY_COLORS[name]
            )
            for name in CATEGORY_NAMES
        ]
    
    def get_all(self) -> List[Category]:
        return list(self._categories)
    
    def get_by_name(self, name: str) -> Optional[Category]:
        for category in self._categories:
            if category.name == name:
                return category
        return None
    
    def get_names(self) -> List[str]:
        return list(CATEGORY_NAMES)
    
    def exists(self, name: str) -> bool:
        return name in CATEGORY_NAMES
    
    def find_by_keyword(self, text: str) -> Optional[Category]:
        text_lower = text.lower()
        for category in self._categories:
            for keyword in category.keywords:
                if keyword.lower() in text_lower:
                    return category
        return None
    
    def count(self) -> int:
        return len(self._categories)
