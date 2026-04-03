from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from typing import Optional
from pydantic import EmailStr


class UserBase(SQLModel,):
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    password: str
    role:str = ""


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creation_date: Optional[datetime] = Field(default=datetime.now(timezone.utc))
    deletion_date: Optional[datetime] = Field(default=None)
    role: str = "Regular User"

class Admin(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str = "Administrator"





