"""Parse resumes pdfs and build a model."""

from bestintern.tools.llm.llm import LiteLLMModels
from bestintern.tools.llm.modeler import LLMDataExtracted, LLMDataExtractor
from bestintern.tools.pdf.reader import PDFReader
from config.models import ResumeMetadata


class ResumeParser:
    def __init__(self, pdf_path: str, llm_model: LiteLLMModels):
        self.pdf_path = pdf_path
        self.llm_model = llm_model
        self.extracted_data = None

    def parse_resume(self) -> LLMDataExtracted:
        # Step 1: Get a resume
        pdf_reader = PDFReader(self.pdf_path)

        # Step 2: Extract data and metadata
        text_content = pdf_reader.get_full_text()

        # Step 3: Ask the LLM to parse through the data
        llm_extractor = LLMDataExtractor(model=self.llm_model)
        extracted_data = llm_extractor.extract_data(text_content, ResumeMetadata)

        self.extracted_data = extracted_data
        return extracted_data

    def save_resume_model(
        self, extracted_data: LLMDataExtracted, output_dir: str
    ) -> None:
        # must save the data in some sort of database lmao
        raise NotImplementedError()
