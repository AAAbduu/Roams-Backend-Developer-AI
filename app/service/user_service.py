from passlib.context import CryptContext
from app.model.user_model import User
from app.repository.user_repository import get_user_repository, UserRepository
from fastapi import Depends
from app.utils.jwt_utils import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, username: str, email: str, password: str) -> User:
        try:
            password = pwd_context.hash(password)
            return self.user_repository.create_user(username, email, password)
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}
        
    def login_user(self, user: User) -> User:
        db_user = self.user_repository.get_user_by_username(user.username)
        if db_user is None or not pwd_context.verify(user.password, db_user.password):
            return {"error": "Invalid credentials"}
        
        access_token = create_access_token(data={"sub": db_user.username, "id": db_user.id})
        return access_token
        
    
def get_user_service(user_repository = Depends(get_user_repository)):
    return UserService(user_repository)
