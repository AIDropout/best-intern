"""Parse job postings from webpages and build a job model."""

from typing import Optional

from bestintern.tools.llm.llm import LiteLLMModels
from bestintern.tools.llm.modeler import LLMDataExtracted, LLMDataExtractor
from bestintern.tools.web.reader import WaitOptions, WebpageReader
from config.models import JobMetadata


class JobParser:
    def __init__(
        self,
        url: str,
        llm_model: LiteLLMModels,
        use_selenium: bool = False,
        wait_options: Optional[WaitOptions] = None,
    ):
        self.url = url
        self.llm_model = llm_model
        self.use_selenium = use_selenium
        self.wait_options = wait_options
        self.extracted_data = None

    def parse_job(self) -> LLMDataExtracted:
        # Step 1: Get a webpage
        webpage_reader = WebpageReader(self.url)

        # Step 2: Read the webpage content
        webpage_reader.read_webpage(
            use_selenium=self.use_selenium, wait_options=self.wait_options
        )
        text_content = webpage_reader.get_text(remove_multiple_newlines=True)

        # Step 3: Extract metadata (if needed)
        metadata = webpage_reader.extract_metadata(
            tags=["meta", "h1", "h2", "p"]
        )  # Example tags

        # Step 4: Ask the LLM to parse through the data
        llm_extractor = LLMDataExtractor(model=self.llm_model)
        extracted_data = llm_extractor.extract_data(text_content, JobMetadata)
        self.extracted_data = extracted_data
        return extracted_data

    def save_job_model(self, extracted_data: LLMDataExtracted, output_dir: str) -> None:
        # just save the data in some sort of database lmao
        raise NotImplementedError()
