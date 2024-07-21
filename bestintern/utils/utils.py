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


def get_fields_info(schema: Dict[str, Any]) -> str:
    """
    Generates a string with information about the fields in a JSON schema.

    Args:
        schema: The JSON schema.

    Returns:
        A formatted string with information about the fields.
    """
    fields_info = ""
    for field, details in schema["properties"].items():
        field_type = details.get("type", "any")
        if "items" in details:
            field_type = f"list of {details['items'].get('type', 'any')}"
        required = field in schema.get("required", [])
        fields_info += (
            f"- {field} ({field_type}{'', required}): "
            f"{details.get('description', 'No description')}\n"
        )
    return fields_info
