import time

from utils.device import screenshot
from utils.img_match import tmpl_load, tmpl_match
from utils.logger import log
from utils.misc import click_until

from . import CONTEXT

_battle_end = "battle-end.png"
_game_over = "game-over.png"
_template = {
    _battle_end: [960 + 85, 640, 105, 80],
    _game_over: [963 + 85, 634, 140, 74],
}


def init():
    tmpl_load("battle_wait", _template)


def run():

    for _ in range(30):
        log.debug("battle wait")
        img = screenshot()

        pos, score = tmpl_match(img, _battle_end)
        if score > 0.7:
            click_until(False, pos, _battle_end)
            CONTEXT.battle_count += 1
            break

        pos, score = tmpl_match(img, _game_over)
        if score > 0.7:
            click_until(False, pos, _game_over)
            # CONTEXT.battle_count = 0
            CONTEXT.is_game_over = True
            log.info(f"game over at round {CONTEXT.battle_count}")
            break

        time.sleep(1)
    log.info(f"round {CONTEXT.battle_count} end")