from utils.device import click, screenshot
from utils.img_match import match, tmpl_load, tmpl_match
from utils.logger import log
from utils.misc import click_until

from . import CONTEXT

# from utils.capture_screen import screenshot

# skill_a: [180, 370, 95, 95]
# skill_b: [280, 300, 95, 95]
# skill_c: [390, 345, 95, 95]

_skill_select = "skill-select.png"
_skill_confirm = "skill-confirm.png"

_skill_roi = [560 - 85, 150, 150, 80]

_skill_a = "rskill-a.png"
_skill_b = "rskill-b.png"
_skill_c = "rskill-c.png"

_pos = [(220 - 85, 420), (320 - 85, 345), (430 - 85, 395)]

_template = {
    _skill_a: _skill_roi,
    _skill_b: _skill_roi,
    _skill_c: _skill_roi,
    _skill_select: [350 - 85, 160, 155, 85],
    _skill_confirm: [695 - 85, 540, 110, 80],
}


# _skill_list: list[bool] = []


def init():
    tmpl_load("skill_select", _template)
    return


# currently it's impossible to live more than 3 rounds, ignore.
# def buttom_choose():
#     pass
# currently it's impossible to live more than 3 rounds, ignore.
# def skill_discard():
#     pass


def skill_choose():
    for pos in _pos:
        click(pos)
        match(_skill_confirm)
        # click_until(True, pos, "skill-confirm.png")
        img = screenshot()
        for skill in [_skill_a, _skill_b, _skill_c]:
            _, score = tmpl_match(img, skill)
            if score > 0.7:
                log.debug(f"found red skill: {skill}")
                return


def run():
    log.info("enter node: skill")
    if CONTEXT.battle_count % 2 == 0:
        match(_skill_select)
        if CONTEXT.battle_count > 6:
            click(_pos[0])
        else:
            skill_choose()
        click(match(_skill_confirm))
    else:
        return

    # currently it's impossible to live more than 4 rounds, ignore.
    # if len(_skill_list) > 3:
    #     skill_discard()
