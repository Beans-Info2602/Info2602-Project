from app.models.user import UserBase
from sqlmodel import SQLModel
from typing import Optional


class UserUpdate(SQLModel):
    username: Optional[str]
 
class AdminCreate(UserBase):
    role:str = "Administrator"

class RegularUserCreate(UserBase):
    role:str = "Regular User"

class UserResponse(SQLModel):
    id: int
    username:str

class SignupRequest(SQLModel):
    username: str
    password: str

from pydantic import BaseModel

class DeleteUsersRequest(BaseModel):
    selected_users: list[int]