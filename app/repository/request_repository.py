import logging
from sqlalchemy.orm import Session
from app.model.request_model import RequestModel
from app.dto.llm_generate_req_dto import GenerateTextRequestDto
from sqlalchemy.exc import IntegrityError
from app.database import get_db_session
from fastapi import Depends

logger = logging.getLogger(__name__)


class RequestRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_request(self, request: GenerateTextRequestDto, payload: dict, result: str) -> RequestModel:
        logger.info(f"Attempting to save request for user with ID: {payload['id']} and prompt: {request.prompt}")
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
            logger.info(f"Request saved successfully for user ID: {payload['id']}")
            return new_request
        except IntegrityError:
            self.db_session.rollback()
            logger.error(f"Integrity error while saving request for user ID: {payload['id']} | Email or Username already exists.")
            raise ValueError("Email or Username already exists.")
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Unexpected error while saving request for user ID: {payload['id']} | Error: {str(e)}")
            raise Exception(f"Error creating request: {str(e)}")

    def get_requests_by_user_id(self, user_id: int):
        logger.info(f"Attempting to retrieve requests for user with ID: {user_id}")
        try:
            requests = self.db_session.query(RequestModel).filter(RequestModel.userId == user_id).all()
            if requests:
                logger.info(f"Found {len(requests)} requests for user ID: {user_id}")
            else:
                logger.warning(f"No requests found for user ID: {user_id}")
            return requests
        except Exception as e:
            logger.error(f"Error retrieving requests for user ID: {user_id} | Error: {str(e)}")
            raise Exception(f"Error retrieving requests: {str(e)}")


def get_request_repository(db_session: Session = Depends(get_db_session)):
    return RequestRepository(db_session)
