import time

from selenium.common import TimeoutException, NoSuchElementException

from actions.resumes_actions.dataframe import build_dataframe, save_dataframe
from actions.resumes_actions.find_resumes import find_resumes
from actions.resumes_actions.parse_resume import parse_resume
from actions.resumes_actions.setup_search import setup_search
from configs.config import config
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def click_resumes():
    setup_search()

    has_next_page = True

    while has_next_page:
        resumes_list = find_resumes()
        if not resumes_list:
            raise Exception("Подходящих резюме не найдено.")

        resume_links = []
        for resume in resumes_list:
            apply_button = resume.find_element(By.XPATH, './/a[@data-qa="serp-item__title"]')
            resume_links.append(apply_button.get_attribute('href'))

        for link in resume_links:
            config.driver.execute_script("window.open(arguments[0], '_blank');", link)
            config.driver.switch_to.window(config.driver.window_handles[-1])

            try:
                resume_data = parse_resume()
                config.resume_records.append(resume_data)
                print(resume_data)
                print(f"Добавлено резюме: {resume_data.get('full_name', 'Неизвестно')}")
            finally:
                config.driver.close()
                config.driver.switch_to.window(config.driver.window_handles[0])

        has_next_page = go_to_next_page()

    dataframe = build_dataframe(config.resume_records)
    if not dataframe.empty:
        save_dataframe(dataframe, config.output_path)
        print(f"Всего сохранено резюме: {len(dataframe)}")
        print(f"Файл с результатами: {config.output_path}")
    else:
        print("Не удалось собрать данные по резюме.")



def go_to_next_page():
    try:
        next_button = config.driver.find_element(By.XPATH, '//a[@data-qa="pager-next"]')
    except NoSuchElementException:
        return False

    classes = (next_button.get_attribute('class') or '').lower()
    if 'disabled' in classes:
        return False

    config.driver.execute_script("arguments[0].click()", next_button)
    try:
        config.wait.until(EC.staleness_of(next_button))
        config.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[contains(@data-qa, "resume-serp__resume") and @data-resume-id]')
            )
        )
    except TimeoutException:
        return False

    time.sleep(1)
    return True