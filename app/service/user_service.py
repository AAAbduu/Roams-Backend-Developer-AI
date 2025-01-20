import logging
from passlib.context import CryptContext
from app.model.user_model import User
from app.repository.user_repository import get_user_repository, UserRepository
from fastapi import Depends
from app.utils.jwt_utils import create_access_token

logger = logging.getLogger(__name__)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, username: str, email: str, password: str) -> User:
        logger.info(f"Attempting to create user with username: {username} and email: {email}")
        try:
            password_hash = pwd_context.hash(password)
            user = self.user_repository.create_user(username, email, password_hash)
            logger.info(f"User created successfully with username: {username}")
            return user
        except ValueError as e:
            logger.error(f"Error creating user with username: {username} | Error: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error creating user with username: {username} | Error: {str(e)}")
            return {"error": str(e)}
        
    def login_user(self, user: User) -> User:
        logger.info(f"Attempting login for user with username: {user.username}")
        try:
            db_user = self.user_repository.get_user_by_username(user.username)
            if db_user is None or not pwd_context.verify(user.password, db_user.password):
                logger.warning(f"Invalid login attempt for user with username: {user.username}")
                return {"error": "Invalid credentials"}
            
            access_token = create_access_token(data={"sub": db_user.username, "id": db_user.id})
            logger.info(f"User logged in successfully with username: {user.username}")
            return access_token
        except Exception as e:
            logger.error(f"Unexpected error during login for user with username: {user.username} | Error: {str(e)}")
            return {"error": "Internal Server Error"}
        
    
def get_user_service(user_repository = Depends(get_user_repository)):
    return UserService(user_repository)
