"""Demo Home page used for showcasing the Page Object Model."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from helpers.selenium_helpers import logger
from pages.base_page import BasePage


class HomePage(BasePage):
    """Simple demo page backed by Selenium's public test form."""

    base_url = BasePage.base_url or "https://www.selenium.dev/selenium/web"
    path = "/web-form.html"

    TEXT_INPUT = (By.NAME, "my-text")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button")
    MESSAGE = (By.ID, "message")

    def open(self) -> "HomePage":
        super().open(self.path)
        return self

    def submit_message(self, value: str) -> str:
        self.type(self.TEXT_INPUT, value, label="Example text input")
        self.click(self.SUBMIT_BUTTON, label="Submit button")
        result = self.get_text(self.MESSAGE, label="Form result")
        logger.info("Form submission result: %s", result)
        return result
