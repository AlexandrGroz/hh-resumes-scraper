from selenium.webdriver.common.by import By

from configs.config import config
from helpers.highlights import highlight_blocks


def find_resumes():
    resumes = config.driver.find_elements(
        By.XPATH,
        '//div[contains(@data-qa, "resume-serp__resume") and @data-resume-id]'
    )
    highlight_blocks(resumes)
    return resumes
