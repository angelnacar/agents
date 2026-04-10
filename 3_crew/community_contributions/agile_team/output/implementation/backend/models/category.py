"""
Modelo de Categoría.
"""

from dataclasses import dataclass, field
from typing import List

from config.categories import CATEGORY_NAMES, CATEGORY_ICONS, CATEGORY_COLORS, CATEGORY_KEYWORDS


@dataclass
class Category:
    """Entidad que representa una categoría de gastos."""
    name: str
    icon: str = ""
    keywords: List[str] = field(default_factory=list)
    color: str = "#6B7280"
    
    def matches_keyword(self, text: str) -> bool:
        """Verifica si el texto contiene alguna palabra clave."""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in self.keywords)
    
    @classmethod
    def from_name(cls, name: str) -> 'Category':
        """Crea una categoría a partir de su nombre."""
        return cls(
            name=name,
            icon=CATEGORY_ICONS.get(name, "💰"),
            keywords=CATEGORY_KEYWORDS.get(name, []),
            color=CATEGORY_COLORS.get(name, "#6B7280")
        )
    
    @classmethod
    def get_all_categories(cls) -> List['Category']:
        """Obtiene todas las categorías del sistema."""
        return [cls.from_name(name) for name in CATEGORY_NAMES]
