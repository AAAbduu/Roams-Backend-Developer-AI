from sqlalchemy.orm import Session
from app.model.request_model import RequestModel
from app.dto.llm_generate_req_dto import GenerateTextRequestDto
from sqlalchemy.exc import IntegrityError
from app.database import get_db_session
from fastapi import Depends

class RequestRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_request(self, request: GenerateTextRequestDto, payload: dict, result: str) -> RequestModel:
        new_request = RequestModel(
            userId=payload["id"],
            prompt=request.prompt,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p,
            generated_text=result
        )
        try:
            self.db_session.add(new_request)
            self.db_session.commit()
            self.db_session.refresh(new_request)
            return new_request
        except IntegrityError:
            self.db_session.rollback()
            raise ValueError("Email or Username already exists.")
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error creating user: {str(e)}")
    
    def get_requests_by_user_id(self, user_id: int):
        return self.db_session.query(RequestModel).filter(RequestModel.userId == user_id).all()
    


def get_request_repository(db_session: Session = Depends(get_db_session)):
    return RequestRepository(db_session)