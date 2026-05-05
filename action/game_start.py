from utils.device import click
from utils.img_match import match, tmpl_load
from utils.logger import log
from utils.misc import click_until

from . import CONTEXT

# from utils.capture_screen import screenshot

_entry = "entry.png"
_select = "select.png"
_start = "start.png"

_character = (680, 405)

_template = {
    _entry: [625, 360, 155, 80],
    # _select: [680, 405, 1, 1],
    _select: [1210, 10, 75, 95],
    # _start: [995, 620, 175, 90],
    _start: [1080, 620, 110, 90],
}


def init():
    tmpl_load("game_start", _template)


def run():
    if CONTEXT.is_game_over:
        CONTEXT.is_game_over = False

        click(match(_entry))
        # select
        match(_select)
        click(_character)
        click_until(False, match(_start), _start)
