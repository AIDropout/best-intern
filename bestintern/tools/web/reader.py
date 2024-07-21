"""Read Webpages and get metadata."""

import re
from time import sleep
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class WaitOptions(BaseModel):
    """Pydantic model for Selenium wait options."""

    element_id: Optional[str] = None
    class_name: Optional[str] = None
    text_content: Optional[str] = None
    html_tag: Optional[str] = None
    html_attribute: Optional[str] = None
    timeout: int = 5


class WebpageReader:
    def __init__(self, url: str):
        self.url = url
        self.text = None
        self.soup = None

    def read_webpage(
        self, use_selenium: bool = False, wait_options: Optional[WaitOptions] = None
    ):
        """Fetches the webpage content and stores the extracted text."""
        if use_selenium:
            self._read_with_selenium(wait_options or WaitOptions())
        else:
            self._read_with_requests()

    def _read_with_requests(self):
        """Read webpage using requests and BeautifulSoup."""
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, "html.parser")
            self.text = self.soup.get_text(separator="\n")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching webpage: {e}")
            self.text = None

    def _read_with_selenium(self, wait_options: WaitOptions):
        """Read webpage using Selenium."""
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get(self.url)

            self._wait_for_element(driver, wait_options)

            self.soup = BeautifulSoup(driver.page_source, "html.parser")
            self.text = self.soup.get_text(separator="\n")
            driver.quit()
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Error fetching webpage with Selenium: {e}")
            self.text = None

    def _wait_for_element(self, driver: WebDriver, wait_options: WaitOptions):
        """Wait for a specific element or content to load."""
        wait = WebDriverWait(driver, wait_options.timeout)

        if wait_options.element_id:
            wait.until(EC.presence_of_element_located((By.ID, wait_options.element_id)))
        elif wait_options.class_name:
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, wait_options.class_name))
            )
        elif wait_options.text_content:
            wait.until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "body"), wait_options.text_content
                )
            )
        elif wait_options.html_tag:
            if wait_options.html_attribute:
                # Wait for specific tag with attribute
                script = (
                    f"return document.querySelector('{wait_options.html_tag}"
                    f"[{wait_options.html_attribute}]') !== null"
                )
            else:
                # Wait for specific tag
                script = (
                    f"return document.querySelector('{wait_options.html_tag}') !== null"
                )
            wait.until(lambda d: d.execute_script(script))
        else:
            sleep(wait_options.timeout)

    def get_text(self, remove_multiple_newlines: bool = False) -> str:
        """Returns the extracted text from the webpage."""
        if not self.text:
            self.read_webpage()
        if remove_multiple_newlines:
            return re.sub(r"\n{2,}", "\n", self.text)
        return self.text

    def extract_metadata(
        self, tags: List[str], delimiter: str = ","
    ) -> dict[str, Optional[str]]:
        """
        Extracts specific metadata from the webpage text based on provided HTML tags.
        """
        if not self.soup:
            self.read_webpage()

        metadata = {}
        for tag in tags:
            data = [element.text.strip() for element in self.soup.find_all(tag)]
            metadata[tag] = delimiter.join(data) if data else None
        return metadata
