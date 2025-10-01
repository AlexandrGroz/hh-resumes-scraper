from configs.config import config
from pages.resumes.search_page import ResumeSearchPage


def setup_search() -> ResumeSearchPage:
    page = ResumeSearchPage(config.driver)
    search_value = (config.search_query or "").strip()
    page.prepare_search(search_value)
    return page
