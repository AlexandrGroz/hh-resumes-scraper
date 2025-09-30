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

    while config.counter < config.limit:
        click_vacancies()

    config.driver.close()
    config.driver.quit()


def start_clicking_resumes():
    click_resumes()



if __name__ == "__main__":
    if is_running_from_batch():
        os.system("cls")

    config.driver.get("https://tyumen.hh.ru/search/resume")

    #start_clicking_vacancies()
    start_clicking_resumes()