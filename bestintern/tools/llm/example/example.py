"""
Example file using Lite LLM.

Steps:
- add .env file based on .env.example
- run `python -m bestintern.tools.llm.example.example`
"""

import json
import os
from pprint import pprint
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel

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
        name: str
        age: Optional[int]
        likes: Optional[List[str]]
        dislikes: Optional[List[str]]
        birthday: Optional[str]

    example_text = """
            Hi, my name's Devanshu. I am 19 years old and I enjoy writing clean code.
            I also like to swim, lift, and sleep. And I love strawberries!!
            I hate not hitting my protein intake. Btw my bday's 10/26/04 ;)
        """

    data_extractor = LLMDataExtractor(model=LiteLLMModels.gemini)
    data = data_extractor.extract_data(text=example_text, model_class=ExampleDataModel)

    pprint(data)


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
    print("\n~ data not found in this job descriptio:")
    print(extracted.not_found)


if __name__ == "__main__":
    print("LiteLLM Example:")
    ex_litellm()

    print("\n\nBasic Modeler Example:")
    ex_modeler()

    print("\n\nJob Description Modeler Example:")
    ex_job_modeler()
