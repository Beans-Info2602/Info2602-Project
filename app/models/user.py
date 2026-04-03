import datetime

from numpy import double
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
    creation_date: Optional[datetime] = Field(default=None)
    deletion_date: Optional[datetime] = Field(default=None)

class Admin(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)





