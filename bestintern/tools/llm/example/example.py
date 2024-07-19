"""
Example file using Lite LLM.

Steps:
- add .env file based on .env.example
- run `python -m bestintern.tools.llm.example.example`
"""

from dotenv import load_dotenv

from bestintern.tools.llm.llm import LiteLLM
from config.models import LiteLLMModels

load_dotenv()


def main():
    litellm = LiteLLM(model=LiteLLMModels.gemini.value)

    response = litellm.askllm(query="what is your name and how old are you?")
    print(response)


if __name__ == "__main__":
    main()
