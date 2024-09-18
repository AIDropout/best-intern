"""
Example file using Lite LLM.

Steps:
- add .env file based on .env.example
- run `python -m bestintern.tools.llm.example.example`
"""

import json
import os
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from bestintern.tools.llm.llm import LiteLLM, LiteLLMModels
from bestintern.tools.llm.modeler import LLMDataExtractor
from config.models import JobMetadata

load_dotenv()


def ex_litellm():
    litellm = LiteLLM(model=LiteLLMModels.gemini)

    response = litellm.askllm(query="what is your name and how old are you?")
    print(response)


def ex_modeler():
    class ExampleDataModel(BaseModel):
        name: str = Field(description="name of subject")
        age: Optional[int] = Field(description="age of subject")
        likes: Optional[List[str]] = Field(description="likes of subject")
        dislikes: Optional[List[str]] = Field(description="dislikes of subject")
        birthday: Optional[str] = Field(description="birthday of subject")

    class Example2(BaseModel):
        rate_code: str = Field(description="identifier for a rate")
        new_rate: str = Field(description="the new interest rate")
        prev_rate: str = Field(description="the previous interest rate")

    example_2 = """
    Hi, my name's Devanshu. I am 19 years old and I enjoy writing clean code.
            I also like to swim, lift, and sleep. And I love strawberries!!
            I hate not hitting my protein intake. Btw my bday's 10/26/04 ;)

    rate identifier: 12345, new rate: 10%
    """

    example_text = """
            Hi, my name's Devanshu. I am 19 years old and I enjoy writing clean code.
            I also like to swim, lift, and sleep. And I love strawberries!!
            I hate not hitting my protein intake. Btw my bday's 10/26/04 ;)
        """

    data_extractor = LLMDataExtractor(model=LiteLLMModels.gemini_flash)
    extracted = data_extractor.extract_data(
        text=example_text, model_class=ExampleDataModel
    )

    print(json.dumps(json.loads(extracted.data.model_dump_json()), indent=2))
    print("\n~ data not found in this description:")
    print(extracted.not_found)

    extracted = data_extractor.extract_data(text=example_2, model_class=Example2)
    print("DANNYS DATA")
    print(json.dumps(json.loads(extracted.data.model_dump_json()), indent=2))
    print("\n~ data not found in this description:")
    print(extracted.not_found)


def ex_job_modeler():
    relative_path = os.path.dirname(os.path.abspath(__file__))
    job_description_path = os.path.join(relative_path, "job_description.txt")
    with open(job_description_path, "r") as file:
        job_description = file.read()

    data_extractor = LLMDataExtractor(model=LiteLLMModels.gemini_flash)
    extracted = data_extractor.extract_data(
        text=job_description, model_class=JobMetadata
    )

    print(json.dumps(json.loads(extracted.data.model_dump_json()), indent=2))
    print("\n~ data not found in this job description:")
    print(extracted.not_found)


if __name__ == "__main__":
    print("LiteLLM Example:")
    ex_litellm()

    print("\n\nBasic Modeler Example:")
    ex_modeler()

    print("\n\nJob Description Modeler Example:")
    ex_job_modeler()
