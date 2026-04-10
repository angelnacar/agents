"""
Repositorio de Gastos.
"""

from typing import Dict, List, Optional
from datetime import datetime

from models.expense import Expense


class ExpenseRepository:
    """Repositorio para gestionar gastos en memoria."""
    
    def __init__(self):
        self._storage: List[Expense] = []
    
    def add(self, expense: Expense) -> Expense:
        self._storage.append(expense)
        return expense
    
    def update(self, expense: Expense) -> Optional[Expense]:
        for i, e in enumerate(self._storage):
            if e.id == expense.id:
                self._storage[i] = expense
                return expense
        return None
    
    def delete(self, expense_id: str) -> bool:
        for i, expense in enumerate(self._storage):
            if expense.id == expense_id:
                del self._storage[i]
                return True
        return False
    
    def get_by_id(self, expense_id: str) -> Optional[Expense]:
        for expense in self._storage:
            if expense.id == expense_id:
                return expense
        return None
    
    def get_all(self) -> List[Expense]:
        return list(self._storage)
    
    def get_by_user(self, user_id: str) -> List[Expense]:
        return [expense for expense in self._storage if expense.user_id == user_id]
    
    def filter(self, user_id: str, filters: Optional[Dict] = None) -> List[Expense]:
        expenses = self.get_by_user(user_id)
        if filters is None:
            return expenses
        
        if 'category' in filters and filters['category']:
            expenses = [e for e in expenses if e.category == filters['category']]
        if 'date_from' in filters and filters['date_from']:
            expenses = [e for e in expenses if e.date >= filters['date_from']]
        if 'date_to' in filters and filters['date_to']:
            expenses = [e for e in expenses if e.date <= filters['date_to']]
        
        return expenses
    
    def get_by_period(self, user_id: str, year: int, month: int) -> List[Expense]:
        expenses = self.get_by_user(user_id)
        return [
            expense for expense in expenses
            if expense.date.year == year and expense.date.month == month
        ]
    
    def count(self) -> int:
        return len(self._storage)
    
    def count_by_user(self, user_id: str) -> int:
        return len([e for e in self._storage if e.user_id == user_id])
    
    def clear(self) -> None:
        self._storage.clear()
    
    def clear_by_user(self, user_id: str) -> None:
        self._storage = [e for e in self._storage if e.user_id != user_id]
