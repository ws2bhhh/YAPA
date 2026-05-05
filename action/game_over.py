from utils.device import click, screenshot
from utils.img_match import tmpl_match

from . import CONTEXT

_btn_next = (950, 610)


def init():
    return


def run():
    if CONTEXT.is_game_over:
        CONTEXT.is_game_over = True
        CONTEXT.battle_count = 0
        while True:
            _, score = tmpl_match(screenshot(), "entry.png")
            if score > 0.7:
                break
            click(_btn_next)
