# Structured JSON output with Pydantic
import os
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# define your output structure
class Summary(BaseModel):
    title: str = Field(..., description="Short title of the summary")
    key_points: list[str] = Field(..., description="List of main points")
    score: float = Field(..., description="Confidence score")

def _get_structured_model():
    """Lazy initialization of structured model"""
    base_model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    return base_model.with_structured_output(Summary)

def get_structured_summary(text: str):
    structured_model = _get_structured_model()
    # model.invoke returns an instance matching Summary
    result = structured_model.invoke(f"Summarize this:\n{text}")
    # since it's a BaseModel, you can access fields directly
    return {
        "title": result.title,
        "key_points": result.key_points,
        "score": result.score
    }

def structured_summary(text: str):
    return get_structured_summary(text)

