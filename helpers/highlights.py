from configs.config import config


def highlight_blocks(elements):
    if elements is None:
        return

    if isinstance(elements, (list, tuple, set)):
        iterable = elements
    else:
        iterable = [elements]

    for element in iterable:
        if element is None:
            continue
        config.driver.execute_script("arguments[0].style.border='3px solid red';", element)
