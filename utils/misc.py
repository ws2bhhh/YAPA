import time

from .device import click, screenshot
from .img_match import tmpl_match


def click_until(mode: bool, pos: tuple[int, int] | None, name: str, timeout: int = 30):
    if pos is None:
        return None

    if mode:
        for _ in range(timeout):
            _, score = tmpl_match(screenshot(), name)
            if score > 0.7:
                return True
            click(pos)
            time.sleep(0.5)
    else:
        for _ in range(timeout):
            _, score = tmpl_match(screenshot(), name)
            if score < 0.7:
                return True
            click(pos)
            time.sleep(0.5)

    if timeout >= 30:
        raise TimeoutError("click_until timeout")

    return None
