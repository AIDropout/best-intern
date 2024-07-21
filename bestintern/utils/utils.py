import json
import os
import re
from datetime import date, datetime
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, Template


def clean_llm_response(response: str) -> str:
    """
    Extracts and cleans a JSON string from an LLM response.

    Args:
        response: The response from the LLM.

    Returns:
        The cleaned JSON string.

    Raises:
        ValueError: If no valid JSON object is found in the response.
    """
    start = response.find("{")
    end = response.rfind("}")

    if start != -1 and end != -1 and start < end:
        json_str = response[start : end + 1]
        json_str = re.sub(r"```json\s*|\s*```", "", json_str)
        return json_str.strip()
    else:
        raise ValueError("No valid JSON object found in the response")


def parse_llm_response(response: str) -> Dict[str, Any]:
    """
    Parses a JSON string from an LLM response into a dictionary.

    Args:
        response: The response from the LLM.

    Returns:
        The parsed JSON data.

    Raises:
        ValueError: If the response is not a valid JSON.
    """
    try:
        cleaned_response = clean_llm_response(response)
        data = json.loads(cleaned_response)
        return data
    except json.JSONDecodeError as jde:
        raise ValueError("LLM response is not a valid JSON") from jde


def parse_date(date_str: str) -> date:
    """
    Parses a date string into a date object.

    Args:
        date_str: The date string in the format 'YYYY-MM-DD'.

    Returns:
        The parsed date object.
    """
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def load_jinja_template(
    template_name: str, templates_dir: str | None = None
) -> Template:
    """
    Loads a Jinja template from the 'templates' directory relative to the calling
    script's location.

    Args:
        template_name: The name of the template file.
        templates_dir: The directory containing the templates folder. If None, defaults
            to the script's directory.

    Returns:
        The loaded Jinja template.
    """
    if templates_dir is None:
        templates_dir = os.path.dirname(os.path.abspath(__file__))
    templates_folder = os.path.join(templates_dir, "templates")
    env = Environment(loader=FileSystemLoader(templates_folder))
    template = env.get_template(template_name)
    return template


def clean_json_structure(data):
    def extract_type(any_of_list):
        for item in any_of_list:
            if "type" in item:
                return item["type"]
        return None

    def simplify_properties(properties):
        simplified = {}
        for key, value in properties.items():
            if "anyOf" in value:
                type_value = extract_type(value["anyOf"])
            else:
                type_value = value.get("type")

            # Only include properties with a type or description
            if type_value or value.get("description"):
                simplified[key] = {
                    "type": type_value,
                    "description": value.get("description"),
                    "default": value.get("default"),
                }
                simplified[key] = {
                    k: v for k, v in simplified[key].items() if v is not None
                }

        return {k: v for k, v in simplified.items() if v}

    def clean_object(obj):
        cleaned = {
            "type": obj.get("type"),
            "properties": simplify_properties(obj.get("properties", {})),
        }
        cleaned = {
            k: v
            for k, v in cleaned.items()
            if v is not None and (not isinstance(v, dict) or v)
        }
        return cleaned

    cleaned_data = {
        key: clean_object(value) for key, value in data.get("$defs", {}).items()
    }

    cleaned_data["properties"] = simplify_properties(data.get("properties", {}))

    # Remove 'title' from all sections if present
    for section in cleaned_data.values():
        section.pop("title", None)

    # If only 'properties' present, return what's inside
    if len(cleaned_data) == 1 and "properties" in cleaned_data:
        return cleaned_data["properties"]
    return cleaned_data
