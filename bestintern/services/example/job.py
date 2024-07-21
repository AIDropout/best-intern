"""
Example file using JobParser.

Steps:
- add .env file based on .env.example
- use sample job application URLs at `job_urls`
- run `python -m bestintern.services.example.job`
"""

from dotenv import load_dotenv

from bestintern.services.parse.job import JobParser, WaitOptions
from bestintern.tools.llm.llm import LiteLLMModels
from bestintern.tools.llm.modeler import LLMDataExtracted

load_dotenv()


def main():
    # URL of the job description page
    job_urls = [
        "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Director--Strategic-Sourcing---Professional-Services_JR1983742",
        "https://www.google.com/about/careers/applications/jobs/results/89830537073435334-senior-software-engineer-mobile-ios-geo",
        "https://careers.tiktok.com/position/7393074791714834739/detail",
    ]

    for job_url in job_urls:
        job_parser = JobParser(
            url=job_url,
            use_selenium=True,
            wait_options=WaitOptions(timeout=5),  # waits for page to load
            llm_model=LiteLLMModels.gemini_flash,
        )

        extracted_data: LLMDataExtracted = job_parser.parse_job()

        print("Extracted Job Data:")
        print(extracted_data.data.model_dump_json(indent=4))


if __name__ == "__main__":
    main()
