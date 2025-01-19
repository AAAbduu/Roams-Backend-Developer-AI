from transformers import pipeline
from app.dto.llm_generate_req_dto import GenerateTextRequestDto

class LLMService:
    def __init__(self):
        self.generator = pipeline("text-generation", model="gpt2")  

    def generate_text(self, request: GenerateTextRequestDto) -> str:
        result = self.generator(
            request.prompt,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p,
            num_return_sequences=1 
        )
        return result[0]["generated_text"]
    
    def get_historical_requests(self, payload: dict):
        print(payload)
        pass

def get_llm_service() -> LLMService:
    return LLMService()
