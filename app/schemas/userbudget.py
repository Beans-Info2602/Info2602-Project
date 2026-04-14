from sqlmodel import Field, SQLModel
from typing import List, Optional
from app.models.userbudget import CategoryName

class UserBudgetCreate(SQLModel):
    name: str
    incomes: List[dict]
    expenses: List[dict]

class UserBudgetUpdate(SQLModel):
    name: Optional[str]
    budget: Optional[float]

class IncomeCreate(SQLModel):
    name: str
    earnings: float
    user_budget_id: int
    
class IncomeUpdate(SQLModel):
    name: Optional[str]
    earnings: Optional[float]
    
class IncomeResponse(SQLModel):
    id: int
    user_budget_id: int
    name: str
    earnings: float
    
class ExpenseCreate(SQLModel):
    name: str
    cost: float
    category: CategoryName = Field(default=CategoryName.OTHER, nullable=False)
    is_recurring: bool = Field(default=False)
    is_paid: bool = Field(default=False)
    user_budget_id: int
    
class ExpenseUpdate(SQLModel):
    name: Optional[str]
    cost: Optional[float]
    category: Optional[CategoryName]
    is_recurring: Optional[bool]
    is_paid: Optional[bool]
    
class ExpenseResponse(SQLModel):
    id: int
    user_budget_id: int
    name: str
    cost: float
    category: CategoryName
    is_recurring: bool
    is_paid: bool
class UserBudgetResponse(SQLModel):
    id: int
    user_id: int
    name: str
    budget: float