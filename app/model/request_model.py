from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class RequestModel(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, index=True, nullable=False)
    prompt = Column(String, nullable=False)
    max_length = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)
    top_p = Column(Float, nullable=False)
    generated_text = Column(String, nullable=False)
