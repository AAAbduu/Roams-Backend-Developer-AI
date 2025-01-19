from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.model.user_model import User
from app.repository.user_repository import get_user_repository, UserRepository
from fastapi import Depends

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, username: str, email: str, password: str) -> User:
        try:
            return self.user_repository.create_user(username, email, password)
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return e
        
    def login_user(self, user: User) -> User:
        db_user = self.user_repository.get_user_by_username(user.username)
        if db_user is None or not pwd_context.verify(user.password, db_user.password):
            return {"error": "Invalid credentials"}
        return db_user.username #here the jwt token should be generated and returned
        
    
def get_user_service(user_repository = Depends(get_user_repository)):
    return UserService(user_repository)
