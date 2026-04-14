from pydantic import BaseModel
from typing import List


class Income(BaseModel):
    name: str
    amount: float


class Expense(BaseModel):
    name: str
    amount: float
    recurring: bool
    category: str


class BudgetCreate(BaseModel):
    name: str
    incomes: List[Income]
    expenses: List[Expense]