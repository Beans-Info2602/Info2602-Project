from datetime import datetime, timezone
from sqlmodel import Relationship, Field, SQLModel
from typing import Optional
from enum import Enum

class CategoryName(str, Enum):
    TECHNOLOGY = "Technology"
    HEALTH = "Health"
    SPORTS = "Sports"
    ENTERTAINMENT = "Entertainment"
    BUSINESS = "Business"
    RENT = "Rent"
    FOOD = "Food"
    UTILITIES = "Utilities"
    OTHER = "Other"

class UserBudget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    name: str = Field(index=True, unique=True)
    budget: Optional[float] = Field(index=True, default=0.0)
    
    income_list: list['Income'] = Relationship(back_populates='user_budget')
    expense_list: list['Expense'] = Relationship(back_populates='user_budget')

class Income(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_budget_id: int = Field(foreign_key='userbudget.id')
    name: str = Field(index=True)
    earnings: float = Field(index=True, default=0.0)
    
    user_budget: UserBudget = Relationship(back_populates='income_list')

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_budget_id: int = Field(foreign_key='userbudget.id')
    category: CategoryName = Field(default=CategoryName.OTHER, nullable=False)
    name: str = Field(index=True)
    cost: float = Field(index=True, default=0.0)
    start_date: Optional[datetime] = Field(default=datetime.now(timezone.utc))
    end_date: Optional[datetime] = Field(default=None)
    is_recurring: bool = Field(default=False)
    is_paid: bool = Field(default=False)
    
    user_budget: UserBudget = Relationship(back_populates='expense_list')
