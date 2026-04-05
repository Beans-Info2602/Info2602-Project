from user import *
from sqlmodel import Enum, Relationship

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
    user_id: int = Field(foreign_key='User.id')
    name: str = Field(index=True, unique=True)
    budget: float = Field(index=True, default=0.0)
    
    incomeList: list['Income'] = Relationship(back_populates='budget')
    expenseList: list['Expense'] = Relationship(back_populates='budget')

class Income(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_account_id: int = Field(foreign_key='UserBudget.id')
    name: str = Field(index=True)
    earnings: float = Field(index=True, default=0.0)
    
    userBudget: UserBudget = Relationship(back_populates='income')

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_account_id: int = Field(foreign_key='UserBudget.id')
    category: CategoryName = Field(default=CategoryName.OTHER, nullable=False)
    name: str = Field(index=True)
    cost: float = Field(index=True, default=0.0)
    start_date: Optional[datetime] = Field(default=datetime.now(timezone.utc))
    end_date: Optional[datetime] = Field(default=None)
    is_recurring: bool = Field(default=False)
    is_paid: bool = Field(default=False)
    
    userBudget: UserBudget = Relationship(back_populates='expense')
