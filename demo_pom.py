"""Demonstration script showing how to use the new Page Object Model helpers."""
from __future__ import annotations

from drivers.set_driver import set_driver
from pages.home_page import HomePage


def run_demo() -> None:
    driver = set_driver()
    page = HomePage(driver)

    try:
        page.open()
        message = page.submit_message("Hello, Selenium!")
        print(f"Demo form responded with: {message}")
    finally:
        driver.quit()


if __name__ == "__main__":
    run_demo()
