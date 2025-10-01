"""Backward compatible highlight helper that proxies to the centralized utilities."""
from __future__ import annotations

from typing import Iterable

from selenium.webdriver.remote.webelement import WebElement

from helpers.selenium_helpers import highlight


def highlight_blocks(elements: WebElement | Iterable[WebElement] | None) -> None:
    """Highlight one or multiple elements when DEBUG_UI is enabled."""
    highlight(elements)
