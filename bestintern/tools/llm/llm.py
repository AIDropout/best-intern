"""Talk to LLMs."""

from enum import Enum

import weave
from litellm import completion
from pydantic import BaseModel


class LiteLLMModels(Enum):
    gemini = "gemini/gemini-pro"  # requires GEMINI_API_KEY
    gemini_flash = "gemini/gemini-1.5-flash"  # requires GEMINI_API_KEY


class LiteLLMConfig(BaseModel):
    model: LiteLLMModels


class LiteLLMResponse(BaseModel):
    content: str


class LiteLLM:
    # weave.init("bestintern")

    def __init__(
        self, model: LiteLLMModels, system_prompt: str = "", num_retries: int = 0
    ) -> None:
        self.model = model.value
        self.system_prompt = system_prompt
        self.num_retries = num_retries

    # @weave.op()
    def askllm(
        self, query: str, overwrite_system_prompt: str = None
    ) -> LiteLLMResponse:

        messages = []

        system_prompt = overwrite_system_prompt or self.system_prompt
        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})

        response = completion(
            model=self.model, messages=messages, num_retries=self.num_retries
        )

        llmresponse = LiteLLMResponse(content=response.choices[0].message.content)
        return llmresponse
