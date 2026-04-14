from app.repositories.user import UserRepository
from app.utilities.security import encrypt_password, verify_password, create_access_token
from app.schemas.user import RegularUserCreate
from typing import Optional

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_all_users(self):
        return self.user_repo.get_all_users()
    
    def get_all_regular_users(self):
        return self.user_repo.get_all_regular_users()

    def get_user_by_id(self, user_id: int):
        return self.user_repo.get_by_id(user_id)
    
    def get_user_by_username(self, username: str):
        return self.user_repo.get_by_username(username)
    
    def search_users(self, query: str, page:int=1, limit:int=10):
        return self.user_repo.search_users(query, page, limit)

    def delete_user(self, user_id: int):
        return self.user_repo.delete_user(user_id)
    