import logging
from sqlalchemy.orm import Session
from app.model.user_model import User
from sqlalchemy.exc import IntegrityError
from app.database import get_db_session
from fastapi import Depends

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_user(self, username: str, email: str, password: str) -> User:
        logger.info(f"Attempting to create user with username: {username} and email: {email}")
        new_user = User(username=username, email=email, password=password)
        try:
            self.db_session.add(new_user)
            self.db_session.commit()
            self.db_session.refresh(new_user)
            logger.info(f"User created successfully with username: {username} and email: {email}")
            return new_user
        except IntegrityError:
            self.db_session.rollback()
            logger.error(f"Integrity error while creating user with username: {username} and email: {email} | Email or Username already exists.")
            raise ValueError("Email or Username already exists.")
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Unexpected error while creating user with username: {username} and email: {email} | Error: {str(e)}")
            raise Exception(f"Error creating user: {str(e)}")

    def get_user_by_username(self, username: str) -> User:
        logger.info(f"Attempting to retrieve user with username: {username}")
        try:
            user = self.db_session.query(User).filter(User.username == username).first()
            if user:
                logger.info(f"User found with username: {username}")
            else:
                logger.warning(f"No user found with username: {username}")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user with username: {username} | Error: {str(e)}")
            raise Exception(f"Error retrieving user: {str(e)}")

    def get_user_by_email(self, email: str) -> User:
        logger.info(f"Attempting to retrieve user with email: {email}")
        try:
            user = self.db_session.query(User).filter(User.email == email).first()
            if user:
                logger.info(f"User found with email: {email}")
            else:
                logger.warning(f"No user found with email: {email}")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user with email: {email} | Error: {str(e)}")
            raise Exception(f"Error retrieving user: {str(e)}")

    def get_user_by_id(self, user_id: int) -> User:
        logger.info(f"Attempting to retrieve user with ID: {user_id}")
        try:
            user = self.db_session.query(User).filter(User.id == user_id).first()
            if user:
                logger.info(f"User found with ID: {user_id}")
            else:
                logger.warning(f"No user found with ID: {user_id}")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user with ID: {user_id} | Error: {str(e)}")
            raise Exception(f"Error retrieving user: {str(e)}")

def get_user_repository(db_session: Session = Depends(get_db_session)):
    return UserRepository(db_session)
