"""
Example file using WebpageReader class

This example demonstrates how to use the WebpageReader class to read a webpage
and extract metadata from specific HTML tags.

Steps:
- replace the urls with the actual URLs of the webpages you want to read
- update the list of tags in `extract_metadata` to match the elements you want data for
   (e.g., ['h1', 'h2'] for titles, ['ul'] for lists)
- update the WaitOptions to match your needs for the webpage
- run `python -m bestintern.tools.web.example.example`
"""

from bestintern.tools.web.reader import WaitOptions, WebpageReader


def main():
    # Example 1: Reading a simple webpage
    url = "https://example.com"
    reader = WebpageReader(url)
    text = reader.get_text(remove_multiple_newlines=True)
    print(f"Text from {url}:\n{text[:500]}...")  # Print first 500 characters

    # Example 2: Extracting metadata
    metadata = reader.extract_metadata(["h1", "p"])
    print("\nMetadata:")
    for tag, content in metadata.items():
        print(f"{tag}: {content}")

    # Example 3: Using Selenium to wait for specific text
    dynamic_url = "https://www.python.org"
    dynamic_reader = WebpageReader(dynamic_url)
    wait_options = WaitOptions(text_content="Compound Data Types", timeout=15)
    dynamic_reader.read_webpage(use_selenium=True, wait_options=wait_options)
    dynamic_text = dynamic_reader.get_text(remove_multiple_newlines=True)
    print(
        f"\nText from {dynamic_url} (using Selenium, waiting for specific text):\n"
        f"{dynamic_text[:500]}..."
    )

    # Example 4: Using Selenium to wait for a specific HTML tag with attribute
    complex_url = "https://www.google.com"
    complex_reader = WebpageReader(complex_url)
    complex_wait_options = WaitOptions(
        html_tag="div", html_attribute="jscontroller", timeout=20
    )
    complex_reader.read_webpage(use_selenium=True, wait_options=complex_wait_options)
    complex_text = complex_reader.get_text(remove_multiple_newlines=True)
    print(
        f"\nText from {complex_url} (using Selenium, waiting for specific HTML tag "
        f"with attribute):\n{complex_text[:500]}..."
    )


if __name__ == "__main__":
    main()
