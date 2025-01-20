from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller import auth_controller, llm_controller
from app.database import Base, engine
import logging



logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('api_requests.log')
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router=auth_controller.router, prefix="/api/auth", tags=["auth"])
app.include_router(router=llm_controller.router, prefix="/api/llm", tags=["llm"])
