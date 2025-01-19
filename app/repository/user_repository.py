from sqlalchemy.orm import Session
from app.model.user_model import User
from sqlalchemy.exc import IntegrityError
from app.database import get_db_session
from fastapi import Depends

class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_user(self, username: str, email: str, password: str) -> User:
        new_user = User(username=username, email=email, password=password)
        try:
            self.db_session.add(new_user)
            self.db_session.commit()
            self.db_session.refresh(new_user)
            return new_user
        except IntegrityError:
            self.db_session.rollback()
            raise ValueError("Email or Username already exists.")
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error creating user: {str(e)}")

    def get_user_by_username(self, username: str) -> User:
        return self.db_session.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> User:
        return self.db_session.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> User:
        return self.db_session.query(User).filter(User.id == user_id).first()

def get_user_repository(db_session: Session = Depends(get_db_session)):
    return UserRepository(db_session)