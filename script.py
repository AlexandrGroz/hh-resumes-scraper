import os

from actions.resumes_actions.click_resumes import click_resumes
from actions.vacancies_actions.click_vacanies import click_vacancies
from actions.login.login import login
from actions.advanced_search.set_advanced_search import set_advanced_search
from configs.config import config
from helpers.check_bat import is_running_from_batch


def start_clicking_vacancies():
    login()
    set_advanced_search()

    limit = getattr(config, "limit", 0)
    while not limit or config.counter < limit:
        click_vacancies()

    config.driver.close()
    config.driver.quit()


def start_clicking_resumes():
    click_resumes()


if __name__ == "__main__":
    if is_running_from_batch():
        os.system("cls")

    try:
        start_clicking_resumes()
    finally:
        try:
            config.driver.quit()
        except Exception:
            pass
