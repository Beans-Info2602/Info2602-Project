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

    def get_user_budget_by_id(self, budget_id: int) -> Optional[UserBudget]:
        return self.db.get(UserBudget, budget_id)

    def get_all_user_budgets(self) -> list[UserBudget]:
        return self.db.exec(select(UserBudget)).all()
    
    def get_all_categories(self) -> list[CategoryName]:
        return list(CategoryName)

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
            self.db.add(income_db)
            self.db.commit()
            self.db.refresh(income_db)
            return income_db
        except Exception as e:
            logger.error(f"An error occurred while adding income: {e}")
            self.db.rollback()
            raise
        
    def add_expense(self, budget_id:int, expense: Expense) -> Expense:
        user_budget = self.db.get(UserBudget, budget_id)
        if not user_budget:
            raise Exception("Invalid user budget id given")
        expense_db = Expense.model_validate(expense)
        expense_db.user_budget_id = budget_id
        try:
            self.db.add(expense_db)
            self.db.commit()
            self.db.refresh(expense_db)
            return expense_db
        except Exception as e:
            logger.error(f"An error occurred while adding expense: {e}")
            self.db.rollback()
            raise