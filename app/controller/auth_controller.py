from fastapi import APIRouter, Depends, HTTPException
from app.service.user_service import get_user_service, UserService
from app.dto.user_dto import UserRegisterDto, UserLoginDto

router = APIRouter()


@router.post("/register")
async def register_user(user: UserRegisterDto, user_service: UserService = Depends(get_user_service)):
    result = user_service.create_user(user.username, user.email, user.password)

    if isinstance(result, dict) and "error" in result:
        if "Email or Username already exists" in result["error"]:
            raise HTTPException(status_code=400, detail=result["error"])
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    return {"message": "User created successfully", "user": result}

    
@router.post("/login")
async def login_user(user: UserLoginDto, user_service: UserService = Depends(get_user_service)):
    result = user_service.login_user(user)
    
    if isinstance(result, dict) and "error" in result:
        if "User not found" in result["error"]:
            raise HTTPException(status_code=400, detail=result["error"])
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    return {"message": "User logged in successfully", "user": result}
