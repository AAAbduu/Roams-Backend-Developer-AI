from fastapi import APIRouter, Depends, HTTPException
from app.dto.llm_generate_req_dto import GenerateTextRequestDto
from app.service.llm_service import LLMService, get_llm_service
from app.utils.jwt_utils import verify_access_token


router = APIRouter()


@router.post("/generate", summary="Generate text using the model")
async def generate_text(request: GenerateTextRequestDto, llm_service: LLMService = Depends(get_llm_service), payload: dict = Depends(verify_access_token)):
    try:
        generated_text = llm_service.generate_text(request, payload)
        return {"prompt": request.prompt, "generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")

@router.get("/history", summary="Get historical requests")
async def get_historical_requests(llm_service: LLMService = Depends(get_llm_service), payload: dict = Depends(verify_access_token)):
    try:
        historical_requests = llm_service.get_historical_requests(payload)
        return {"historical_requests": historical_requests}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting historical requests: {str(e)}")