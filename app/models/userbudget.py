from category import *
from user import *
from sqlmodel import Relationship

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
    earnings: float = Field(index=True, default=0.0)
    
    userBudget: UserBudget = Relationship(back_populates='income')

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_account_id: int = Field(foreign_key='UserBudget.id')
    category_id: int = Field(foreign_key='Category.id')
    cost: float = Field(index=True, default=0.0)
    start_date: Optional[datetime] = Field(default=datetime.now(datetime.timezone.utc))
    end_date: Optional[datetime] = Field(default=None)
    is_recurring: bool = Field(default=False)
    is_paid: bool = Field(default=False)
    
    category: Category = Relationship(back_populates='expenseList')
    userBudget: UserBudget = Relationship(back_populates='expense')
