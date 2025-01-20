import logging
from transformers import pipeline
from app.dto.llm_generate_req_dto import GenerateTextRequestDto
from app.repository.request_repository import RequestRepository, get_request_repository
from fastapi import Depends

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, request_repository: RequestRepository):
        self.generator = pipeline("text-generation", model="gpt2")
        self.request_repository = request_repository

    def generate_text(self, request: GenerateTextRequestDto, payload: dict) -> str:
        logger.info(f"Starting text generation for user {payload.get('sub')} with prompt: {request.prompt[:30]}...")

        try:
            result = self.generator(
                request.prompt,
                max_length=request.max_length,
                temperature=request.temperature,
                top_p=request.top_p,
                num_return_sequences=1 
            )

            generated_text = result[0]["generated_text"]
            self.request_repository.save_request(request, payload, generated_text)

            logger.info(f"Text generated for prompt: {request.prompt[:30]}... | Generated text: {generated_text[:30]}...")
            return generated_text
        except Exception as e:
            logger.error(f"Error generating text for prompt: {request.prompt[:30]}... | Error: {str(e)}")
            raise e
    
    def get_historical_requests(self, payload: dict) -> list:
        logger.info(f"Fetching historical requests for user {payload.get('sub')}")
        try:
            historical_requests = self.request_repository.get_requests_by_user_id(payload["id"])
            logger.info(f"Found {len(historical_requests)} historical requests for user {payload.get('sub')}")
            return historical_requests
        except Exception as e:
            logger.error(f"Error fetching historical requests for user {payload.get('sub')}: {str(e)}")
            raise e


def get_llm_service(requestRepository: RequestRepository = Depends(get_request_repository)) -> LLMService:
    return LLMService(request_repository=requestRepository)
