"""
Example file using PDFReader.

Steps:
- place a "sample_resume.pdf" resume in the same directory as this script
- run `python -m bestintern.tools.pdf.example.example`
"""

import os

from bestintern.tools.pdf.reader import PDFReader


def main():
    # Get the path to the PDF file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, "sample_resume.pdf")
    pdf_reader = PDFReader(pdf_path)

    print(f"Total pages in the PDF: {pdf_reader.get_total_pages()}")
    print("\nFull text content:")
    print(
        pdf_reader.get_full_text()[:500] + "[more in resume...]"
    )  # Print first 500 characters

    print("\nText from the first page:")
    print(
        pdf_reader.get_text_by_page(0)[:300] + "[more in resume...]"
    )  # Print first 300 characters

    print("\nSearching for 'experience':")
    search_results = pdf_reader.search_text("experience")
    for result in search_results[:3]:  # Print first 3 results
        print(f"Page {result['page']}: {result['context']}")

    print("\nExtracted email addresses:")
    print(pdf_reader.extract_emails())

    print("\nExtracted phone numbers:")
    print(pdf_reader.extract_phone_numbers())

    print("\nExtracted metadata:")
    metadata = pdf_reader.extract_metadata()
    for key, value in metadata.items():
        print(f"\n{key.capitalize()}:")
        if isinstance(value, list):
            for item in value[:5]:  # Print first 5 items
                print(f"  - {item}")
        elif isinstance(value, dict):
            for item in value[:5]:  # Print first 5 items
                print(f"  - {item['period']}: {item['description'][:100]}...")
        if len(value) > 5:
            print("    [more in resume...]")

    print("\nText statistics:")
    print(pdf_reader.get_text_statistics())


if __name__ == "__main__":
    main()
