from utils.device import click, screenshot
from utils.img_match import match_all
from utils.logger import log

from . import CONTEXT

"""
#NODE_TO_ACTS = {
    "game_start": 0,
    "skill_select": 1,
    "task": 2,
    "store": 3,
    "battle": 4,
    "battle_wait": 5,
    "game_over": 6,
}
"""


def run(node_to_index: dict[str, int])-> None | int:
    result = match_all(screenshot())
    if result is None:
        log.error("relocate fail")
        return None
    else:
        log.info("relocate success")
        key, node = result
    # repair unfinished node:
    if node == "store":
        node = "battle"

    return node_to_index[node]
