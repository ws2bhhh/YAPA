import time

from utils.img_match import match, tmpl_load
from utils.logger import log
from utils.misc import click_until

from . import CONTEXT

_task_select = "task-select.png"
# _task_confirm = "task-confirm.png"
_task_complete = "task-complete.png"

_btn_task = (640, 620)

_template = {
    _task_select: [545, 25, 185, 85],
    # _task_confirm: [640, 620, 1, 1],
    # _task_complete: [590, 580, 100, 75],
    _task_complete: [520, 125, 75, 70],
}


def init():
    tmpl_load("task", _template)


def run():
    log.info("enter node: task")
    if CONTEXT.battle_count == 1:
        match(_task_select)
    elif CONTEXT.battle_count > 1:
        # may trigger by relocate
        if match(_task_complete, False) is None:
            return
    click_until(False, _btn_task, _task_complete)
