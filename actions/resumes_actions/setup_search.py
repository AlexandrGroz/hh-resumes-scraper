from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from configs.config import config
from helpers.highlights import highlight_blocks


def setup_search():
    search_input = config.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="a11y-search-input"]'))
    )
    highlight_blocks(search_input)

    search_value = (config.search_query or "").strip()
    config.driver.execute_script("arguments[0].value = arguments[1]", search_input, search_value)

    search_button = config.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="search-button"]'))
    )
    highlight_blocks(search_button)
    config.driver.execute_script("arguments[0].click()", search_button)

    config.wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//div[contains(@data-qa, "resume-serp__resume") and @data-resume-id]')
        )
    )
