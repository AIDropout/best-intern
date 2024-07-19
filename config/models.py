from enum import Enum

from pydantic import BaseModel


class LiteLLMModels(Enum):
    gemini = "gemini/gemini-pro"  # requires GEMINI_API_KEY


class LiteLLMConfig(BaseModel):
    model: LiteLLMModels


class LiteLLMResponse(BaseModel):
    content: str
