from pydantic import BaseModel, Field
from typing import Optional

class GenerateTextRequestDto(BaseModel):
    prompt: str = Field(..., min_length=1, description="Input text for the model to generate a response.")
    max_length: Optional[int] = Field(50, ge=1, le=1000, description="Maximum length of the generated text.")
    temperature: Optional[float] = Field(1.0, ge=0.0, le=2.0, description="Controls randomness: lower values make output more deterministic.")
    top_p: float = Field(0.9, ge=0.0, le=1.0, description="Controls diversity via nucleus sampling. Lower values make the output more focused.")
