from configs.config import config
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from helpers.highlights import highlight_blocks


def setup_search():
    search_input= config.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="a11y-search-input"]')))
    highlight_blocks(search_input)
    config.driver.execute_script('arguments[0].value = arguments[1]', search_input, config.search_query)

    #Click search button
    advanced_search_apply_button = config.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="search-button"]')))
    config.driver.execute_script("arguments[0].click()", advanced_search_apply_button)