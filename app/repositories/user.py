from sqlmodel import Session, select, func
from app.models.user import Admin, UserBase, User
from app.models.userbudget import UserBudget, Income, Expense
from typing import Optional, Tuple
from app.utilities.pagination import Pagination
from app.schemas.user import UserUpdate
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: UserBase) -> Optional[User]:
        try:
            user_db = User.model_validate(user_data)
            self.db.add(user_db)
            self.db.commit()
            self.db.refresh(user_db)
            return user_db
        except Exception as e:
            logger.error(f"An error occurred while saving user: {e}")
            self.db.rollback()
            raise

    def search_users(self, query: str, page:int=1, limit:int=10) -> Tuple[list[User], Pagination]:
        offset = (page - 1) * limit
        db_qry = select(User)
        if query:
            db_qry = db_qry.where(
                User.username.ilike(f"%{query}%")
            )
        count_qry = select(func.count()).select_from(db_qry.subquery())
        count_todos = self.db.exec(count_qry).one()

        users = self.db.exec(db_qry.offset(offset).limit(limit)).all()
        pagination = Pagination(total_count=count_todos, current_page=page, limit=limit)

        return users, pagination

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.exec(select(User).where(User.username == username)).one_or_none()

    def get_by_username_any(self, username: str) -> Optional[User | Admin]:
        user = self.get_by_username(username)
        if user:
            return user
        return self.db.exec(select(Admin).where(Admin.username == username)).one_or_none()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.get(User, user_id)

    def get_by_id_and_role(self, user_id: int, role: str) -> Optional[User | Admin]:
        if role == "Administrator":
            return self.db.get(Admin, user_id)
        return self.db.get(User, user_id)

    def get_all_users(self) -> list[User]:
        return self.db.exec(select(User)).all()
    
    def get_all_regular_users(self) -> list[User]:
        return self.db.exec(select(User).where(User.role == "Regular User")).all()

    def update_user(self, user_id:int, user_data: UserUpdate)->User:
        user = self.db.get(User, user_id)
        if not user:
            raise Exception("Invalid user id given")
        if user_data.username:
            user.username = user_data.username
        
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            logger.error(f"An error occurred while updating user: {e}")
            self.db.rollback()
            raise

    def delete_user(self, user_id: int):
        user = self.db.get(User, user_id)
        if not user:
            raise Exception("User doesn't exist")
        if user.role == "Administrator":
            raise Exception("Admin users cannot be deleted")
        try:
            user_budgets = self.db.exec(
                select(UserBudget).where(UserBudget.user_id == user_id)
            ).all()

            for budget in user_budgets:
                expenses = self.db.exec(
                    select(Expense).where(Expense.user_budget_id == budget.id)
                ).all()
                for expense in expenses:
                    self.db.delete(expense)

                incomes = self.db.exec(
                    select(Income).where(Income.user_budget_id == budget.id)
                ).all()
                for income in incomes:
                    self.db.delete(income)

                self.db.delete(budget)

            self.db.delete(user)
            self.db.commit()
        except Exception as e:
            logger.error(f"An error occurred while deleting user: {e}")
            self.db.rollback()
            raise
