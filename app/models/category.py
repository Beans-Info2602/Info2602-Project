from sqlmodel import Field, SQLModel
from typing import Optional
from enum import Enum

class CategoryName(str, Enum):
    Income = 'income'
    Expense = 'expense'

class Category(SQLModel, Enum, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_name: CategoryName = Field(default=None, nullable=False)
