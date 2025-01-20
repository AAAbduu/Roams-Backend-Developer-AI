from transformers import pipeline
from app.dto.llm_generate_req_dto import GenerateTextRequestDto
from app.repository.request_repository import RequestRepository, get_request_repository
from fastapi import Depends

class LLMService:
    def __init__(self , request_repository: RequestRepository):
        self.generator = pipeline("text-generation", model="gpt2")
        self.request_repository = request_repository

    def generate_text(self, request: GenerateTextRequestDto, payload: dict) -> str:
        result = self.generator(
            request.prompt,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p,
            num_return_sequences=1 
        )
        self.request_repository.save_request(request, payload, result[0]["generated_text"])
        return result[0]["generated_text"]
    
    def get_historical_requests(self, payload: dict) -> list:
        return self.request_repository.get_requests_by_user_id(payload["id"])
        
        
def get_llm_service(requestRepository: RequestRepository = Depends(get_request_repository)) -> LLMService:
    return LLMService(request_repository=requestRepository)
