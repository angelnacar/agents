"""
Servicio de Gestión de Gastos.
"""

from typing import Dict, List, Optional
from datetime import datetime

from models.expense import Expense
from models.base import Result
from repositories.expense_repository import ExpenseRepository
from services.categorization_service import CategorizationService


class ExpenseService:
    """Servicio de gestión de gastos que implementa operaciones CRUD."""
    
    def __init__(
        self,
        expense_repository: ExpenseRepository,
        categorization_service: CategorizationService
    ):
        self._repository = expense_repository
        self._categorization = categorization_service
    
    def create_expense(
        self,
        user_id: str,
        description: str,
        amount: float,
        date: datetime,
        category: Optional[str] = None
    ) -> Result:
        """Crea un nuevo gasto para el usuario especificado."""
        if amount is None or amount <= 0:
            return Result.fail("El monto es obligatorio y debe ser mayor a 0")
        
        if date is None:
            return Result.fail("La fecha es obligatoria")
        
        if date > datetime.now():
            return Result.fail("La fecha no puede ser futura")
        
        if description and len(description) > 200:
            return Result.fail("La descripción no puede exceder 200 caracteres")
        
        if category is None or category == "":
            auto_category = self._categorization.categorize(description)
            category = auto_category.name
        
        try:
            expense = Expense(
                user_id=user_id,
                description=description or "",
                amount=float(amount),
                date=date,
                category=category
            )
            self._repository.add(expense)
            return Result.ok(expense)
        except ValueError as e:
            return Result.fail(str(e))
    
    def update_expense(
        self,
        expense_id: str,
        user_id: str,
        description: Optional[str] = None,
        amount: Optional[float] = None,
        date: Optional[datetime] = None,
        category: Optional[str] = None
    ) -> Result:
        """Actualiza un gasto existente."""
        expense = self._repository.get_by_id(expense_id)
        
        if expense is None:
            return Result.fail("El gasto no fue encontrado", "EXPENSE_NOT_FOUND")
        
        if expense.user_id != user_id:
            return Result.fail("No tienes permiso para editar este gasto", "UNAUTHORIZED")
        
        new_description = description if description is not None else expense.description
        new_amount = amount if amount is not None else expense.amount
        new_date = date if date is not None else expense.date
        
        if amount is not None and amount <= 0:
            return Result.fail("El monto debe ser positivo")
        
        if category is None or category == "":
            auto_category = self._categorization.categorize(new_description)
            category = auto_category.name
        
        try:
            expense.update(
                description=new_description,
                amount=new_amount,
                date=new_date,
                category=category
            )
            self._repository.update(expense)
            return Result.ok(expense)
        except ValueError as e:
            return Result.fail(str(e))
    
    def delete_expense(self, expense_id: str, user_id: str) -> Result:
        """Elimina un gasto existente."""
        expense = self._repository.get_by_id(expense_id)
        
        if expense is None:
            return Result.fail("El gasto no fue encontrado", "EXPENSE_NOT_FOUND")
        
        if expense.user_id != user_id:
            return Result.fail("No tienes permiso para eliminar este gasto", "UNAUTHORIZED")
        
        success = self._repository.delete(expense_id)
        
        if success:
            return Result.ok(True)
        return Result.fail("No se pudo eliminar el gasto")
    
    def get_expenses(
        self,
        user_id: str,
        category: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> List[Expense]:
        """Obtiene la lista de gastos del usuario con filtros opcionales."""
        filters = {}
        
        if category:
            filters['category'] = category
        
        if date_from:
            filters['date_from'] = date_from
        
        if date_to:
            filters['date_to'] = date_to
        
        if filters:
            return self._repository.filter(user_id, filters)
        
        return self._repository.get_by_user(user_id)
    
    def get_expense_by_id(self, expense_id: str, user_id: str) -> Optional[Expense]:
        """Obtiene un gasto específico por su ID."""
        expense = self._repository.get_by_id(expense_id)
        
        if expense and expense.user_id == user_id:
            return expense
        
        return None
    
    def get_user_expenses_for_period(
        self,
        user_id: str,
        year: int,
        month: int
    ) -> List[Expense]:
        """Obtiene todos los gastos del usuario para un período específico."""
        expenses = self._repository.get_by_period(user_id, year, month)
        return sorted(expenses, key=lambda x: x.date, reverse=True)
