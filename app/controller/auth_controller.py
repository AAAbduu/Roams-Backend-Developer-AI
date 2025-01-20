from fastapi import APIRouter, Depends, HTTPException
from app.service.user_service import get_user_service, UserService
from app.dto.user_dto import UserRegisterDto, UserLoginDto
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/register")
async def register_user(user: UserRegisterDto, user_service: UserService = Depends(get_user_service)):
    logger.info(f"Request to register user: {user.username} with email: {user.email}")
    
    result = user_service.create_user(user.username, user.email, user.password)

    if isinstance(result, dict) and "error" in result:
        logger.error(f"Error during registration for {user.username}: {result['error']}")
        if "Email or Username already exists" in result["error"]:
            raise HTTPException(status_code=400, detail=result["error"])
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    logger.info(f"User {user.username} created successfully")
    return {"message": "User created successfully", "user": result}

    
@router.post("/login")
async def login_user(user: UserLoginDto, user_service: UserService = Depends(get_user_service)):
    logger.info(f"Login attempt for user: {user.username}")

    result = user_service.login_user(user)
    
    if isinstance(result, dict) and "error" in result:
        logger.error(f"Login failed for {user.username}: {result['error']}")
        if "User not found" in result["error"]:
            raise HTTPException(status_code=400, detail=result["error"])
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    logger.info(f"Login successful for user: {user.username}")
    return {"access_token": result, "token_type": "bearer"}
