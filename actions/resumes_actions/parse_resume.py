from urllib.parse import urlparse

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from configs.config import config


def parse_resume():
    resume_data = {
        'resume_id': extract_resume_id(config.driver.current_url),
        'url': config.driver.current_url,
        'desired_position': safe_get_text(By.XPATH, '//span[@data-qa="resume-block-title-position"]'),
        'salary': safe_get_text(By.XPATH, '//span[@data-qa="resume-block-salary"]'),
        'age': safe_get_text(By.XPATH, '//span[@data-qa="resume-personal-age"]'),
        'gender': safe_get_text(By.XPATH, '//span[@data-qa="resume-personal-gender"]'),
        'location': safe_get_text(By.XPATH, '//span[@data-qa="resume-personal-address"]'),
        'work_experience': safe_get_text(By.XPATH, '//div[@data-qa="resume-block-experience"]'),
        'education': safe_get_text(By.XPATH, '//div[@data-qa="resume-block-education"]'),
        'languages': safe_join_texts(By.XPATH, '//span[@data-qa="resume-block-language-item"]'),
        'skills': safe_join_texts(By.XPATH, '//span[@data-qa="skills-table-item"]'),
        'citizenship': safe_join_texts(By.XPATH, '//span[@data-qa="resume-personal-citizenship"]'),
        'ready_to_relocate': safe_get_text(By.XPATH, '//p[@data-qa="resume-personal-relocation"]'),
        'travel_time': safe_get_text(By.XPATH, '//span[@data-qa="resume-personal-metro"]'),
        'updated_at': safe_get_text(By.XPATH, '//span[@data-qa="resume-updatedAt"]'),
    }

    return resume_data


def safe_get_text(by, selector):
    try:
        element = config.driver.find_element(by, selector)
        return element.text.strip()
    except NoSuchElementException:
        return ''


def safe_join_texts(by, selector, separator=', '):
    try:
        elements = config.driver.find_elements(by, selector)
    except NoSuchElementException:
        return ''

    values = [element.text.strip() for element in elements if element.text.strip()]
    return separator.join(values)


def extract_resume_id(url):
    parsed = urlparse(url)
    resume_id = parsed.path.rstrip('/').split('/')[-1]
    return resume_id