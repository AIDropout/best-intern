"""Read PDFs and get metadata."""

import io
import re
from typing import Dict, List, Union

import PyPDF2


class PDFReader:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.pdf_reader = None
        self.text_content = ""
        self.pages = []
        self.file_handle = None
        self.initialize_reader()

    def initialize_reader(self):
        """Initialize the PDF reader object."""
        try:
            if isinstance(self.pdf_file, str):
                # If pdf_file is a file path
                self.file_handle = open(self.pdf_file, "rb")
                self.pdf_reader = PyPDF2.PdfReader(self.file_handle)
            elif isinstance(self.pdf_file, io.BytesIO):
                # If pdf_file is a BytesIO object
                self.pdf_reader = PyPDF2.PdfReader(self.pdf_file)
            else:
                raise ValueError(
                    "Unsupported file type. Please provide a file path or "
                    "BytesIO object."
                )

            self.extract_all_text()
        except Exception as e:
            if self.file_handle:
                self.file_handle.close()
            raise Exception(  # pylint: disable=broad-exception-raised
                f"Error initializing PDF reader: {str(e)}"
            ) from e

    def extract_all_text(self):
        """Extract text from all pages of the PDF."""
        try:
            for page in self.pdf_reader.pages:
                page_text = page.extract_text()
                self.pages.append(page_text)
                self.text_content += page_text + "\n"
        except Exception as e:
            raise Exception(  # pylint: disable=broad-exception-raised
                f"Error extracting text from PDF: {str(e)}"
            ) from e

    def get_full_text(self) -> str:
        """Return the full text content of the PDF."""
        return self.text_content.strip()

    def get_text_by_page(self, page_num: int) -> str:
        """Return the text content of a specific page."""
        if 0 <= page_num < len(self.pages):
            return self.pages[page_num].strip()
        else:
            raise ValueError(f"Invalid page number. Total pages: {len(self.pages)}")

    def get_total_pages(self) -> int:
        """Return the total number of pages in the PDF."""
        return len(self.pages)

    def search_text(self, search_term: str) -> List[Dict[str, Union[int, str]]]:
        """
        Search for a term in the PDF and return a list of occurrences with page numbers.
        """
        results = []
        for page_num, page_text in enumerate(self.pages):
            if search_term.lower() in page_text.lower():
                results.append(
                    {
                        "page": page_num + 1,
                        "context": self.get_context(page_text, search_term),
                    }
                )
        return results

    def get_context(
        self, text: str, search_term: str, context_length: int = 100
    ) -> str:
        """Helper method to get context around a search term."""
        search_index = text.lower().index(search_term.lower())
        start = max(0, search_index - context_length)
        end = min(len(text), search_index + len(search_term) + context_length)
        return text[start:end].strip()

    def extract_emails(self) -> List[str]:
        """Extract all email addresses from the PDF."""
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return list(set(re.findall(email_pattern, self.text_content)))

    def extract_phone_numbers(self) -> List[str]:
        """Extract all phone numbers from the PDF."""
        phone_pattern = (
            r"\b(?:\+?1[-.]?)?\(?[2-9][0-8][0-9]\)?[-.]?[2-9][0-9]{2}[-.]?[0-9]{4}\b"
        )
        return list(set(re.findall(phone_pattern, self.text_content)))

    def extract_location(self) -> List[str]:
        """Extract potential location information from the PDF."""
        # This pattern looks for common location formats (City, State ZIP)
        location_pattern = (
            r"\b(?:[A-Z][a-z]+(?:\s[A-Z][a-z]+)*,\s*[A-Z]{2}\s*\d{5}(?:-\d{4})?)\b"
        )
        return list(set(re.findall(location_pattern, self.text_content)))

    def extract_education(self) -> List[str]:
        """Extract education information from the PDF."""
        education_keywords = r"\b(?:degree|bachelor|master|phd|diploma|certificate)\b"
        education_sections = re.split(
            education_keywords, self.text_content, flags=re.IGNORECASE
        )
        education_info = []
        for section in education_sections[
            1:
        ]:  # Skip the first section as it's before any keyword
            lines = section.strip().split("\n")
            if lines:
                education_info.append(
                    lines[0].strip()
                )  # Add the first line after each keyword
        return education_info

    def extract_work_experience(self) -> List[Dict[str, str]]:
        """Extract work experience information from the PDF."""
        experience_pattern = (
            r"(\b(?:January|February|March|April|May|June|July|"
            r"August|September|October|November|December)\s\d{4}"
            r"\s*-\s*(?:January|February|March|April|May|June|July|"
            r"August|September|October|November|December)\s\d{4}|"
            r"\bPresent\b)\s*(.*?)(?=\n\n|\Z)"
        )
        experiences = re.findall(experience_pattern, self.text_content, re.DOTALL)

        return [
            {"period": exp[0].strip(), "description": exp[1].strip()}
            for exp in experiences
        ]

    def extract_skills(self) -> List[str]:
        """Extract potential skills from the PDF."""
        skill_pattern = r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b"
        potential_skills = re.findall(skill_pattern, self.text_content)
        # Filter out common words that are likely not skills
        common_words = set(
            [
                "The",
                "And",
                "Or",
                "In",
                "On",
                "At",
                "To",
                "For",
                "With",
                "By",
                "From",
                "Up",
                "About",
                "Into",
                "Over",
                "After",
            ]
        )
        return list(
            set(skill for skill in potential_skills if skill not in common_words)
        )

    def extract_metadata(self) -> Dict[str, Union[List[str], List[Dict[str, str]]]]:
        """Extract all metadata from the PDF."""
        return {
            "emails": self.extract_emails(),
            "phone_numbers": self.extract_phone_numbers(),
            "locations": self.extract_location(),
            "education": self.extract_education(),
            "work_experience": self.extract_work_experience(),
            "skills": self.extract_skills(),
        }

    def get_text_statistics(self) -> Dict[str, int]:
        """Return basic statistics about the text content."""
        words = self.text_content.split()
        return {
            "total_words": len(words),
            "unique_words": len(set(words)),
            "total_characters": len(self.text_content),
            "total_pages": self.get_total_pages(),
        }

    def __str__(self):
        return f"PDFReader object: {self.get_total_pages()} pages"

    def __repr__(self):
        return self.__str__()

    def __del__(self):
        """Destructor to ensure file is closed when object is deleted."""
        if self.file_handle:
            self.file_handle.close()
