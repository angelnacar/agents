"""
Servicio de Estadísticas.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

from models.expense import Expense
from repositories.expense_repository import ExpenseRepository


class StatisticsService:
    """Servicio de estadísticas y cálculos agregados de gastos."""
    
    def __init__(self, expense_repository: ExpenseRepository):
        self._repository = expense_repository
    
    def get_total_expenses(self, user_id: str, year: int, month: int) -> float:
        """Calcula el total de gastos para un período específico."""
        expenses = self._repository.get_by_period(user_id, year, month)
        return sum(expense.amount for expense in expenses)
    
    def get_expenses_by_category(self, user_id: str, year: int, month: int) -> Dict[str, float]:
        """Obtiene la distribución de gastos por categoría."""
        expenses = self._repository.get_by_period(user_id, year, month)
        result: Dict[str, float] = {}
        
        for expense in expenses:
            if expense.category not in result:
                result[expense.category] = 0.0
            result[expense.category] += expense.amount
        
        return result
    
    def get_average_expense(self, user_id: str, year: int, month: int) -> float:
        """Calcula el gasto promedio por transacción."""
        expenses = self._repository.get_by_period(user_id, year, month)
        if not expenses:
            return 0.0
        return sum(expense.amount for expense in expenses) / len(expenses)
    
    def get_expense_count(self, user_id: str, year: int, month: int) -> int:
        """Cuenta el número de transacciones en un período."""
        return len(self._repository.get_by_period(user_id, year, month))
    
    def get_top_category(self, user_id: str, year: int, month: int) -> Optional[Dict[str, Any]]:
        """Identifica la categoría con mayor gasto."""
        expenses_by_category = self.get_expenses_by_category(user_id, year, month)
        
        if not expenses_by_category:
            return None
        
        total = sum(expenses_by_category.values())
        if total == 0:
            return None
        
        top_category_name = max(expenses_by_category, key=expenses_by_category.get)
        top_amount = expenses_by_category[top_category_name]
        
        from config.categories import CATEGORY_ICONS
        icon = CATEGORY_ICONS.get(top_category_name, "💰")
        
        return {
            "name": top_category_name,
            "icon": icon,
            "total": top_amount,
            "percentage": (top_amount / total) * 100
        }
    
    def get_daily_average(self, user_id: str, year: int, month: int) -> float:
        """Calcula el gasto promedio por día en el período."""
        from calendar import monthrange
        total = self.get_total_expenses(user_id, year, month)
        days_in_month = monthrange(year, month)[1]
        return total / days_in_month if days_in_month > 0 else 0.0
    
    def get_max_expense(self, user_id: str, year: int, month: int) -> Optional[float]:
        """Obtiene el gasto máximo en el período."""
        expenses = self._repository.get_by_period(user_id, year, month)
        if not expenses:
            return None
        return max(expense.amount for expense in expenses)
    
    def get_min_expense(self, user_id: str, year: int, month: int) -> Optional[float]:
        """Obtiene el gasto mínimo en el período."""
        expenses = self._repository.get_by_period(user_id, year, month)
        if not expenses:
            return None
        return min(expense.amount for expense in expenses)
    
    def get_statistics_summary(self, user_id: str, year: int, month: int) -> Dict[str, Any]:
        """Genera un resumen completo de estadísticas."""
        total = self.get_total_expenses(user_id, year, month)
        count = self.get_expense_count(user_id, year, month)
        average = self.get_average_expense(user_id, year, month)
        top_category = self.get_top_category(user_id, year, month)
        by_category = self.get_expenses_by_category(user_id, year, month)
        
        return {
            "total": total,
            "count": count,
            "average": average,
            "daily_average": self.get_daily_average(user_id, year, month),
            "max_expense": self.get_max_expense(user_id, year, month),
            "min_expense": self.get_min_expense(user_id, year, month),
            "top_category": top_category,
            "by_category": by_category,
            "year": year,
            "month": month
        }
    
    def get_chart_data(self, user_id: str, year: int, month: int) -> Dict[str, Any]:
        """Genera datos optimizados para renderizado de gráficos."""
        by_category = self.get_expenses_by_category(user_id, year, month)
        total = sum(by_category.values())
        
        if total == 0:
            return {
                "labels": [],
                "values": [],
                "colors": [],
                "total": 0
            }
        
        from config.categories import CATEGORY_COLORS, CATEGORY_ICONS
        
        labels = []
        values = []
        colors = []
        
        for category_name, amount in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            labels.append(f"{CATEGORY_ICONS.get(category_name, '💰')} {category_name}")
            values.append(amount)
            colors.append(CATEGORY_COLORS.get(category_name, "#6B7280"))
        
        return {
            "labels": labels,
            "values": values,
            "colors": colors,
            "total": total
        }
