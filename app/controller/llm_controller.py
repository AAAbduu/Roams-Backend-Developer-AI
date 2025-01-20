from fastapi import APIRouter, Depends, HTTPException
from app.dto.llm_generate_req_dto import GenerateTextRequestDto
from app.service.llm_service import LLMService, get_llm_service
from app.utils.jwt_utils import verify_access_token
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/generate", summary="Generate text using the model")
async def generate_text(request: GenerateTextRequestDto, llm_service: LLMService = Depends(get_llm_service), payload: dict = Depends(verify_access_token)):
    logger.info(f"Request to generate text received: {request.prompt[:30]}... for user {payload.get('sub')}")
    
    try:
        generated_text = llm_service.generate_text(request, payload)
        logger.info(f"Generated text: {generated_text[:30]}... for prompt: {request.prompt[:30]}...")
        return {"prompt": request.prompt, "generated_text": generated_text}
    
    except Exception as e:
        logger.error(f"Error generating text for prompt {request.prompt[:30]}...: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")

@router.get("/history", summary="Get historical requests")
async def get_historical_requests(llm_service: LLMService = Depends(get_llm_service), payload: dict = Depends(verify_access_token)):
    logger.info(f"Request to get historical requests for user {payload.get('sub')}")
    
    try:
        historical_requests = llm_service.get_historical_requests(payload)
        logger.info(f"Retrieved {len(historical_requests)} historical requests for user {payload.get('sub')}")
        return {"historical_requests": historical_requests}
    
    except Exception as e:
        logger.error(f"Error getting historical requests for user {payload.get('sub')}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting historical requests: {str(e)}")
