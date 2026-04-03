from user import *
from sqlmodel import Relationship
from numpy import double

class UserBudget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='User.id')
    name: str = Field(index=True, unique=True)
    budget: double = Field(index=True, default=0.0)
    incomeList: list['Income'] = Relationship(back_populates='budget')
    expenseList: list['Expense'] = Relationship(back_populates='budget')

class Income(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_account_id: int = Field(foreign_key='UserBudget.id')
    userBudget: UserBudget = Relationship(back_populates='income')

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_account_id: int = Field(foreign_key='UserBudget.id')
    category_id: int = Field(foreign_key='Category.id')
    userBudget: UserBudget = Relationship(back_populates='income')
