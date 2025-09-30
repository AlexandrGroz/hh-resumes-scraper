import os

from dotenv import load_dotenv
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from drivers.set_driver import set_driver

load_dotenv()


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.counter = 0
            cls._instance.wait_time = 10
            cls._instance.login_url = "https://hh.ru/account/login"
            cls._instance.base_page = "https://hh.ru"
            cls._instance.driver_type = os.getenv("DRIVER", "chrome").lower()
            cls._instance.driver = set_driver(cls._instance.driver_type)
            cls._instance.action = ActionChains(cls._instance.driver)
            cls._instance.wait = WebDriverWait(cls._instance.driver, cls._instance.wait_time)
            cls._instance.search_query = os.getenv("SEARCH_QUERY", "")
            cls._instance.limit = int(os.getenv("LIMIT", "0") or 0)
            cls._instance.resume_records = []
            cls._instance.output_path = os.getenv("OUTPUT_PATH", "data/resumes.csv")

        return cls._instance

    def increment_counter(self):
        self.counter += 1


config = Config()
