import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from .auth_bearer import JWTBearer
from fastapi.security import HTTPAuthorizationCredentials



load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"  
ACCESS_TOKEN_EXPIRE_MINUTES = 30  #minutes
oauth2_scheme = JWTBearer()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> dict:
    try:
        token_bytes = credentials.credentials.encode('utf-8')
        payload = jwt.decode(token_bytes, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
        



