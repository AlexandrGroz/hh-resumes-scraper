from configs.config import config


def highlight_blocks(elements):
    if not isinstance(elements, (list, tuple)):
        elements = [elements]

    for element in elements:
        config.driver.execute_script("arguments[0].style.border='3px solid red';", element)

