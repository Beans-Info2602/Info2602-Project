from sqlmodel import Session, select
from app.models.userbudget import *
from typing import Optional
from app.schemas.userbudget import UserBudgetUpdate
import logging

logger = logging.getLogger(__name__)

class UserBudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user_budget(self, user_budget: UserBudget) -> UserBudget:
        user_budget_db = UserBudget.model_validate(user_budget)
        try:
            self.db.add(user_budget_db)
            self.db.commit()
            self.db.refresh(user_budget_db)
            return user_budget_db
        except Exception as e:
            logger.error(f"An error occurred while saving user budget: {e}")
            self.db.rollback()
            raise
        
    def delete_user_budget(self, budget_id:int):
        user_budget = self.db.get(UserBudget, budget_id)
        if not user_budget:
            raise Exception("Invalid user budget id given")
        try:
            self.db.delete(user_budget)
            self.db.commit()
        except Exception as e:
            logger.error(f"An error occurred while deleting user budget: {e}")
            self.db.rollback()
            raise

    def get_user_budget_by_id(self, budget_id: int) -> Optional[UserBudget]:
        return self.db.get(UserBudget, budget_id)

    def get_all_budgets_for_user(self, user_id: int) -> list[UserBudget]:
        return self.db.exec(select(UserBudget).where(UserBudget.user_id == user_id)).all()
    
    def get_budget_for_user(self, user_id: int) -> Optional[UserBudget]:
        return self.db.exec(select(UserBudget).where(UserBudget.user_id == user_id)).one_or_none()
    
    def get_all_categories(self) -> list[CategoryName]:
        return list(CategoryName)
    
    def get_total_budget_for_user(self, user_id:int) -> float:
        user_budgets = self.db.exec(select(UserBudget).where(UserBudget.user_id == user_id)).all()
        return sum(budget.budget for budget in user_budgets)
    
    def get_budget_amount_for_user(self, budget_id:int, user_id:int) -> float:
        budget = self.db.exec(select(UserBudget).where(UserBudget.user_id == user_id, UserBudget.id == budget_id)).one_or_none()
        if not budget:
            raise Exception("Invalid user budget id given")
        return budget.budget

    def update_user_budget(self, budget_id:int, user_budget_data: UserBudgetUpdate)->UserBudget:
        user_budget = self.db.get(UserBudget, budget_id)
        if not user_budget:
            raise Exception("Invalid user budget id given")
        if user_budget_data.name:
            user_budget.name = user_budget_data.name
        
        try:
            self.db.add(user_budget)
            self.db.commit()
            self.db.refresh(user_budget)
            return user_budget
        except Exception as e:
            logger.error(f"An error occurred while updating user budget: {e}")
            self.db.rollback()
            raise
        
    def add_income(self, budget_id:int, income: Income) -> Income:
        user_budget = self.db.get(UserBudget, budget_id)
        if not user_budget:
            raise Exception("Invalid user budget id given")
        income_db = Income.model_validate(income)
        income_db.user_budget_id = budget_id
        try:
            new_budget = user_budget.budget + income.earnings
            user_budget.budget = new_budget
            self.db.add(income_db)
            self.db.commit()
            self.db.refresh(income_db)
            return income_db
        except Exception as e:
            logger.error(f"An error occurred while adding income: {e}")
            self.db.rollback()
            raise
        
    def update_income(self, income_id:int, income_data: Income) -> Income:
        income = self.db.get(Income, income_id)
        if not income:
            raise Exception("Invalid income id given")
        if income_data.name:
            income.name = income_data.name
        if income_data.earnings:
            income.earnings = income_data.earnings
            budget = self.db.get(UserBudget, income.user_budget_id)
            new_budget = budget.budget - income.earnings + income_data.earnings
            budget.budget = new_budget

        try:
            self.db.add(income)
            self.db.commit()
            self.db.refresh(income)
            return income
        except Exception as e:
            logger.error(f"An error occurred while updating income: {e}")
            self.db.rollback()
            raise
    
    def delete_income(self, income_id:int):
        income = self.db.get(Income, income_id)
        budget = self.db.get(UserBudget, income.user_budget_id)
        if not income:
            raise Exception("Invalid income id given")
        try:
            new_budget = budget.budget - income.earnings
            budget.budget = new_budget
            self.db.delete(income)
            self.db.commit()
        except Exception as e:
            logger.error(f"An error occurred while deleting income: {e}")
            self.db.rollback()
            raise
        
    def get_all_incomes_for_budget(self, budget_id:int) -> list[Income]:
        return self.db.exec(select(Income).where(Income.user_budget_id == budget_id)).all()
        
    def add_expense(self, budget_id:int, expense: Expense) -> Expense:
        user_budget = self.db.get(UserBudget, budget_id)
        if not user_budget:
            raise Exception("Invalid user budget id given")
        expense_db = Expense.model_validate(expense)
        expense_db.user_budget_id = budget_id
        try:
            new_budget = user_budget.budget - expense.cost
            user_budget.budget = new_budget
            self.db.add(expense_db)
            self.db.commit()
            self.db.refresh(expense_db)
            return expense_db
        except Exception as e:
            logger.error(f"An error occurred while adding expense: {e}")
            self.db.rollback()
            raise
        
    def update_expense(self, expense_id:int, expense_data: Expense) -> Expense:
        expense = self.db.get(Expense, expense_id)
        if not expense:
            raise Exception("Invalid expense id given")
        if expense_data.name:
            expense.name = expense_data.name
        if expense_data.cost:
            expense.cost = expense_data.cost
            budget = self.db.get(UserBudget, expense.user_budget_id)
            new_budget = budget.budget + expense.cost - expense_data.cost
            budget.budget = new_budget
        if expense_data.category:
            expense.category = expense_data.category
        if expense_data.start_date:
            expense.start_date = expense_data.start_date
        if expense_data.end_date:
            expense.end_date = expense_data.end_date
        if expense_data.is_recurring is not None:
            expense.is_recurring = expense_data.is_recurring
        if expense_data.is_paid is not None:
            expense.is_paid = expense_data.is_paid
        
        try:
            self.db.add(expense)
            self.db.commit()
            self.db.refresh(expense)
            return expense
        except Exception as e:
            logger.error(f"An error occurred while updating expense: {e}")
            self.db.rollback()
            raise
        
    def get_all_expenses_for_budget(self, budget_id:int) -> list[Expense]:
        return self.db.exec(select(Expense).where(Expense.user_budget_id == budget_id)).all()
    
    def get_all_expenses_by_category_for_budget(self, budget_id:int, category: CategoryName) -> list[Expense]:
        return self.db.exec(select(Expense).where(Expense.user_budget_id == budget_id, Expense.category == category)).all()
    
    def get_all_recurring_expenses_for_budget(self, budget_id:int) -> list[Expense]:
        return self.db.exec(select(Expense).where(Expense.user_budget_id == budget_id, Expense.is_recurring == True)).all()
    
    def get_all_non_recurring_expenses_for_budget(self, budget_id:int) -> list[Expense]:
        return self.db.exec(select(Expense).where(Expense.user_budget_id == budget_id, Expense.is_recurring == False)).all()
    
    def get_all_unpaid_expenses_for_budget(self, budget_id:int) -> list[Expense]:
        return self.db.exec(select(Expense).where(Expense.user_budget_id == budget_id, Expense.is_paid == False)).all()
    
    def delete_expense(self, expense_id:int):
        expense = self.db.get(Expense, expense_id)
        budget = self.db.get(UserBudget, expense.user_budget_id)
        if not expense:
            raise Exception("Invalid expense id given")
        try:
            new_budget = budget.budget + expense.cost
            budget.budget = new_budget
            self.db.delete(expense)
            self.db.commit()
        except Exception as e:
            logger.error(f"An error occurred while deleting expense: {e}")
            self.db.rollback()
            raise