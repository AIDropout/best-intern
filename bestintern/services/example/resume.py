"""
Example file using ResumeParser.

Steps:
- add .env file based on .env.example
- use a sample PDF resume file, rn its `basic_cs_freak.pdf`
- run `python -m bestintern.services.example.resume`
"""

import os

from dotenv import load_dotenv

from bestintern.services.parse.resume import ResumeParser
from bestintern.tools.llm.llm import LiteLLMModels
from bestintern.tools.llm.modeler import LLMDataExtracted

load_dotenv()


def main():
    # Path to the PDF resume file
    relative_path = os.path.dirname(os.path.abspath(__file__))
    pdf_path = "basic_cs_freak.pdf"

    resume_parser = ResumeParser(
        pdf_path=os.path.join(relative_path, pdf_path),
        llm_model=LiteLLMModels.gemini_flash,
    )

    extracted_data: LLMDataExtracted = resume_parser.parse_resume()

    print("Extracted Resume Data:")
    print(extracted_data.data.model_dump_json(indent=4))


if __name__ == "__main__":
    main()
