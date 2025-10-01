"""Page object for the resume detail view."""
from __future__ import annotations

from urllib.parse import urlparse

from selenium.webdriver.common.by import By

from helpers.selenium_helpers import find_all, logger
from pages.base_page import BasePage


class ResumeDetailPage(BasePage):
    """Encapsulates selectors and helpers for resume details."""

    FULL_NAME = (By.XPATH, '//h1[@data-qa="resume-personal-name"]')
    DESIRED_POSITION = (By.XPATH, '//span[@data-qa="resume-block-title-position"]')
    SALARY = (By.XPATH, '//span[@data-qa="resume-block-salary"]')
    AGE = (By.XPATH, '//span[@data-qa="resume-personal-age"]')
    GENDER = (By.XPATH, '//span[@data-qa="resume-personal-gender"]')
    LOCATION = (By.XPATH, '//span[@data-qa="resume-personal-address"]')
    WORK_EXPERIENCE = (By.XPATH, '//div[@data-qa="resume-block-experience"]')
    EDUCATION = (By.XPATH, '//div[@data-qa="resume-block-education"]')
    LANGUAGES = (By.XPATH, '//span[@data-qa="resume-block-language-item"]')
    SKILLS = (By.XPATH, '//span[@data-qa="skills-table-item"]')
    CITIZENSHIP = (By.XPATH, '//span[@data-qa="resume-personal-citizenship"]')
    READY_TO_RELOCATE = (By.XPATH, '//p[@data-qa="resume-personal-relocation"]')
    TRAVEL_TIME = (By.XPATH, '//span[@data-qa="resume-personal-metro"]')
    UPDATED_AT = (By.XPATH, '//span[@data-qa="resume-updatedAt"]')

    def collect(self) -> dict:
        logger.info("Collecting resume details from %s", self.current_url)
        return {
            "resume_id": self._extract_resume_id(self.current_url),
            "url": self.current_url,
            "full_name": self.get_optional_text(self.FULL_NAME, label="Full name"),
            "desired_position": self.get_optional_text(self.DESIRED_POSITION, label="Desired position"),
            "salary": self.get_optional_text(self.SALARY, label="Salary"),
            "age": self.get_optional_text(self.AGE, label="Age"),
            "gender": self.get_optional_text(self.GENDER, label="Gender"),
            "location": self.get_optional_text(self.LOCATION, label="Location"),
            "work_experience": self.get_optional_text(self.WORK_EXPERIENCE, label="Work experience"),
            "education": self.get_optional_text(self.EDUCATION, label="Education"),
            "languages": self._join_texts(self.LANGUAGES, label="Languages"),
            "skills": self._join_texts(self.SKILLS, label="Skills"),
            "citizenship": self._join_texts(self.CITIZENSHIP, label="Citizenship"),
            "ready_to_relocate": self.get_optional_text(
                self.READY_TO_RELOCATE, label="Relocation readiness"
            ),
            "travel_time": self.get_optional_text(self.TRAVEL_TIME, label="Travel time"),
            "updated_at": self.get_optional_text(self.UPDATED_AT, label="Updated at"),
        }

    def _join_texts(self, locator, *, label: str, separator: str = ", ") -> str:
        elements = find_all(self.driver, locator, label=label, timeout=1, require=False)
        values = [element.text.strip() for element in elements if element.text.strip()]
        return separator.join(values)

    @staticmethod
    def _extract_resume_id(url: str) -> str:
        parsed = urlparse(url)
        return parsed.path.rstrip("/").split("/")[-1]
