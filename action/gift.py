import time

from utils.img_match import match, tmpl_load
from utils.logger import log
from utils.misc import click_until

from . import CONTEXT

_gift_select = "gift-select.png"

_btn_task = (640, 620)

_template = {
    _gift_select: [545, 25, 185, 85],
}


def init():
    tmpl_load("gift", _template)


def run():
    log.info("enter node: gift")
    if CONTEXT.battle_count == 0:
        match(_gift_select)
    else:
        # may trigger by relocate
        if match(_gift_select, False) is None:
            return
    click_until(False, _btn_task, _gift_select)
    time.sleep(1)