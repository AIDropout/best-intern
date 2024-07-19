"""Talk to LLMs."""

from litellm import completion

from config.models import LiteLLMModels, LiteLLMResponse


class LiteLLM:
    def __init__(
        self, model: LiteLLMModels, system_prompt: str = "", num_retries: int = 0
    ) -> None:
        self.model = model
        self.system_prompt = system_prompt
        self.num_retries = num_retries

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
