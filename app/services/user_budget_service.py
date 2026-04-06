from app.repositories.userbudget import UserBudgetRepository
from app.schemas.userbudget import *
from typing import Optional

class UserBudgetService:
    def __init__(self, user_budget_repo: UserBudgetRepository):
        self.user_budget_repo = user_budget_repo

    def create_user_budget(self, user_budget: UserBudgetCreate) -> UserBudgetResponse:
        return self.user_budget_repo.create_user_budget(user_budget)
    
    def update_user_budget(self, budget_id:int, user_budget_data: UserBudgetUpdate)->UserBudgetResponse:
        return self.user_budget_repo.update_user_budget(budget_id, user_budget_data)
    
    def get_total_budget_for_user(self, user_id:int) -> float:
        return self.user_budget_repo.get_total_budget_for_user(user_id)
    
    def get_budget_amount_for_user(self, budget_id:int, user_id:int) -> float:
        return self.user_budget_repo.get_budget_amount_for_user(budget_id, user_id)
    
    def delete_user_budget(self, budget_id:int):
        self.user_budget_repo.delete_user_budget(budget_id)

    def get_user_budget_by_id(self, budget_id: int) -> Optional[UserBudgetResponse]:
        return self.user_budget_repo.get_user_budget_by_id(budget_id)

    def get_all_user_budgets(self) -> list[UserBudgetResponse]:
        return self.user_budget_repo.get_all_user_budgets()
    
    def get_all_categories(self) -> list[CategoryName]:
        return self.user_budget_repo.get_all_categories()

    def update_user_budget(self, budget_id:int, user_budget_data: UserBudgetUpdate)->UserBudgetResponse:
        return self.user_budget_repo.update_user_budget(budget_id, user_budget_data)
    
    def add_income(self, income: IncomeCreate) -> IncomeResponse:
        return self.user_budget_repo.add_income(income)
    
    def get_all_incomes_for_budget(self, user_budget_id:int) -> list[IncomeResponse]:
        return self.user_budget_repo.get_all_incomes_for_budget(user_budget_id)
    
    def update_income(self, income_id:int, income_data: IncomeUpdate) -> IncomeResponse:
        return self.user_budget_repo.update_income(income_id, income_data)
    
    def delete_income(self, income_id:int):
        self.user_budget_repo.delete_income(income_id)
        
    def add_expense(self, expense: ExpenseCreate) -> ExpenseResponse:
        return self.user_budget_repo.add_expense(expense)
    
    def get_all_expenses_for_budget(self, user_budget_id:int) -> list[ExpenseResponse]:
        return self.user_budget_repo.get_all_expenses_for_budget(user_budget_id)
    
    def update_expense(self, expense_id:int, expense_data: ExpenseUpdate) -> ExpenseResponse:
        return self.user_budget_repo.update_expense(expense_id, expense_data)
    
    def delete_expense(self, expense_id:int):
        self.user_budget_repo.delete_expense(expense_id)
        
    def get_all_expenses_by_category_for_budget(self, user_budget_id:int, category: CategoryName) -> list[ExpenseResponse]:
        return self.user_budget_repo.get_all_expenses_by_category_for_budget(user_budget_id, category)