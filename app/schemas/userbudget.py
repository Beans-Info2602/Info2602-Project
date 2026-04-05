from sqlmodel import Field, SQLModel
from typing import Optional
from app.models.userbudget import CategoryName

class UserBudgetUpdate(SQLModel):
    name: Optional[str]
    
class IncomeCreate(SQLModel):
    name: str
    earnings: float
    
class ExpenseCreate(SQLModel):
    name: str
    cost: float
    category: CategoryName = Field(default=CategoryName.OTHER, nullable=False)
    is_recurring: bool = Field(default=False)
    is_paid: bool = Field(default=False)
    
class UserBudgetResponse(SQLModel):
    id: int
    user_id: int
    name: str
    budget: float