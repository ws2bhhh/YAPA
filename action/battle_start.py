from utils.img_match import match, tmpl_load
from utils.logger import log
from utils.misc import click_until

_battle = "battle.png"

_template = {_battle: [1060 + 85, 625, 100, 80]}


def init():
    tmpl_load("battle", _template)


def run():
    pos = match(_battle)
    # while match(_battle, False) is not None:
    #     click(pos)
    click_until(False, pos, _battle)
