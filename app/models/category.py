from sqlmodel import Field, SQLModel
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

class Category(SQLModel, Enum, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_name: CategoryName = Field(default=None, nullable=False)
