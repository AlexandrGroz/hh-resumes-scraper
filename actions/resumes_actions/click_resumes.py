from actions.resumes_actions.dataframe import build_dataframe, save_dataframe
from actions.resumes_actions.find_resumes import find_resumes
from actions.resumes_actions.parse_resume import parse_resume
from actions.resumes_actions.setup_search import setup_search
from configs.config import config
from helpers.selenium_helpers import logger


def click_resumes():
    search_page = setup_search()

    config.resume_records = []

    resume_limit = getattr(config, "resume_limit", 0)

    while not resume_limit or len(config.resume_records) < resume_limit:
        resumes_list = list(find_resumes(search_page))
        if not resumes_list:
            raise Exception("Подходящих резюме не найдено.")

        resume_links = search_page.extract_resume_links(resumes_list)
        if not resume_links:
            logger.info("На странице не найдено ссылок на резюме")
            break

        for link in resume_links:
            if resume_limit and len(config.resume_records) >= resume_limit:
                logger.info("Достигнут лимит сбора резюме: %s", resume_limit)
                break

            logger.info("Открываем резюме в новой вкладке: %s", link)
            config.driver.execute_script("window.open(arguments[0], '_blank');", link)
            config.driver.switch_to.window(config.driver.window_handles[-1])

            try:
                resume_data = parse_resume()
            except Exception as error:  # pragma: no cover - depends on remote site
                logger.exception("Не удалось распарсить резюме: %s", error)
            else:
                config.resume_records.append(resume_data)
                logger.info("Добавлено резюме: %s", resume_data.get("full_name", "Неизвестно"))
                print(resume_data)
            finally:
                config.driver.close()
                config.driver.switch_to.window(config.driver.window_handles[0])

        if resume_limit and len(config.resume_records) >= resume_limit:
            logger.info("Достигнут лимит резюме: %s", resume_limit)
            break

        if not search_page.go_to_next_page():
            break

    dataframe = build_dataframe(config.resume_records)
    if not dataframe.empty:
        save_dataframe(dataframe, config.output_path)
        print(f"Всего сохранено резюме: {len(dataframe)}")
        print(f"Файл с результатами: {config.output_path}")
    else:
        print("Не удалось собрать данные по резюме.")
