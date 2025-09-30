import time

from actions.resumes_actions.find_resumes import find_resumes
from actions.resumes_actions.setup_search import setup_search
from configs.config import config
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def click_resumes():
    setup_search()

    resumes_list = find_resumes()
    if len(resumes_list) > 0:
        print()
        for resume in resumes_list:
            apply_button = resume.find_element(By.XPATH, './/a[@data-qa="serp-item__title"]')
            a = apply_button.get_attribute('href')
            config.driver.execute_script("window.open('');")
            config.driver.switch_to.window(config.driver.window_handles[1])
            config.driver.get(a)
            #config.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "main-content")]')))
            time.sleep(1)
            #config.increment_counter()
            #config.driver.close()
            #config.driver.switch_to.window(config.driver.window_handles[0])
    else:
        raise Exception("Подходящих резюме не найдено.")
