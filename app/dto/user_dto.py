from pydantic import BaseModel

class UserLoginDto(BaseModel):
    username: str
    password: str
        
        
        
class UserRegisterDto(BaseModel):
    email: str
    username: str
    password: str