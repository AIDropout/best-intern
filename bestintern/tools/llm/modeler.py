"""Organize unordered text into Pydantic Models."""

import os
from typing import Any, Dict, List, Type, TypeVar

from pydantic import BaseModel, ValidationError

from bestintern.tools.llm.llm import LiteLLM, LiteLLMModels
from bestintern.utils.utils import (
    clean_json_structure,
    load_jinja_template,
    parse_llm_response,
)

T = TypeVar("T", bound=BaseModel)

MAX_ATTEMPTS = 2


class LLMDataExtracted(BaseModel):
    data: T
    not_found: list


class LLMDataExtractor:
    def __init__(self, model: LiteLLMModels, max_retries: int = MAX_ATTEMPTS):
        self.llm = LiteLLM(model=model, num_retries=max_retries)

    def extract_data(
        self, text: str, model_class: Type[T], preprocess: bool = False
    ) -> LLMDataExtracted:
        if preprocess:
            text = self._preprocess_text(text, model_class)

        prompt = self._generate_prompt(text, model_class)

        for attempt in range(MAX_ATTEMPTS):
            try:
                response = self.llm.askllm(prompt)
                data = parse_llm_response(response.content)
                extracted_data = model_class(**data)
                missing_fields = self._get_missing_fields(data, model_class)
                return LLMDataExtracted(data=extracted_data, not_found=missing_fields)
            except (ValidationError, ValueError) as e:
                if attempt == MAX_ATTEMPTS - 1:
                    raise ValueError(
                        f"Failed to extract valid data after {MAX_ATTEMPTS} attempts: "
                        f"{str(e)}"
                    ) from e

                error_prompt = (
                    f"The previous attempt failed due to: {str(e)}. "
                    "Please try again, ensuring all required fields are filled "
                    "and the format is correct. Provide only the JSON object, "
                    "without any additional text before or after it."
                )
                prompt += f"\n\n{error_prompt}"

        raise ValueError("Unexpected error in data extraction process")

    def _preprocess_text(self, text: str, model_class: Type[T]) -> str:
        """Organizes data from the text in more readable formatting using model_class"""
        raise NotImplementedError("this funtion is yet to be implemented")

    def _generate_prompt(self, text: str, model_class: Type[T]) -> str:
        schema = model_class.model_json_schema()
        fields_info = clean_json_structure(schema)
        template_dir = os.path.dirname(os.path.abspath(__file__))
        template = load_jinja_template("extract_data.j2", template_dir)
        return template.render(fields_info=fields_info, text=text)

    def _get_missing_fields(
        self, data: Dict[str, Any], model_class: Type[T]
    ) -> List[str]:
        schema = model_class.model_json_schema()
        all_fields = set(schema["properties"].keys())
        provided_fields = {k for k, v in data.items() if v not in (None, "", [], {})}
        missing_fields = list(all_fields - provided_fields)
        return missing_fields
