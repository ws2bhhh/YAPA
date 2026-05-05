import time

import cv2
import numpy as np

from utils.device import click, screenshot
from utils.img_match import match, smart_delay, tmpl_load, tmpl_match
from utils.logger import log
from utils.misc import click_until

from . import CONTEXT

_store = "store.png"
_buy = "buy.png"
_buy_slot = "buy-slot.png"
_sale = "sale.png"

_btn_refresh = (425 - 85, 595)
_btn_buy_slot = (770, 520)
_empty_pos = (50, 580)

_template = {
    _store: [265, 160, 100, 80],
    _buy: [745 - 85, 555, 95, 75],
    _buy_slot: [670 + 30, 330, 90, 75],
    _sale: [0],
}


def init():
    tmpl_load("store", _template)


# 0,1,2,4,8...
# _refresh_count = 0
"""
a: 204 363 t200
b: 290 353
c: 376 343 
d: 462 333 

e: 218 493 t150
f: 304 483 t200
g: 390 473
h: 476 463

"""
_goods_pos = {
    "a": (204 - 89, 364 - 1),
    "b": (290 - 89, 354 - 1),
    "c": (376 - 89, 344 - 1),
    "d": (462 - 89, 334 - 1),
    "e": (218 - 89, 494 - 1),
    "f": (304 - 89, 484 - 1),
    "g": (390 - 89, 474 - 1),
    "h": (476 - 89, 464 - 1),
}

_red_goods: list[str] = []

_slot_pos = {
    # right
    "0": (608, 176),
    "1": (569, 254),
    "2": (554, 339),
    "3": (569, 423),
    "4": (608, 500),
    # left
    "5": (1002, 176),
    "6": (1040, 254),
    "7": (1058, 340),
    "8": (1045, 423),
    "9": (1001, 501),
}

_empty_slots: list[str] = []
_will_sale: list[str] = []
_unlocked_slots: int = 0


def goods_detect():
    global _red_goods

    # reset
    _red_goods.clear()
    hsv_img = cv2.cvtColor(screenshot(), cv2.COLOR_BGR2HSV)
    for key in _goods_pos.keys():
        x, y = _goods_pos[key]
        h, s, v = hsv_img[y, x]
        # red:
        log.debug(f"pos: {x}, {y} hsv: {h}, {s}, {v}")
        if (h <= 10 or h >= 160) and s > 50 and v > 50:
            log.debug(f"red goods pos: {key}")
            _red_goods.append(key)
    if len(_red_goods) > 0:
        return True

    # refresh store page
    return False


def slots_detect():
    global _empty_slots
    global _will_sale

    # reset
    _empty_slots.clear()
    click(_empty_pos)

    img = screenshot()
    for key in _slot_pos.keys():
        x, y = _slot_pos[key]
        r, g, b = img[y, x]
        bright = np.sum([r, g, b])
        if bright < 150:
            if key in _will_sale:
                _will_sale.remove(key)
            _empty_slots.append(key)

    if len(_empty_slots) > 0:
        log.debug(f"slot {_empty_slots} is empty")
        return True
    else:
        log.debug("no empty slots")
        return False


def sale_and_buy():
    # global _empty_slots
    global _unlocked_slots
    global _will_sale

    # sale
    slots_detect()  # clean slots that fail to fill
    for pos in _will_sale:
        log.debug(f"sale slot: {pos}")

        if int(pos) > 4:
            # left
            roi = [635, 400, 120, 300]
        else:
            # right
            roi = [190, 400, 120, 300]

        click(_slot_pos[pos])
        smart_delay(_sale)
        btn_pos, score = tmpl_match(screenshot(), _sale, roi)
        if score > 0.7:
            smart_delay(_sale, True)
            click_until(False, btn_pos, _sale)
        else:
            smart_delay(_sale, False)
            log.debug("sale failed")

    # buy slot
    if CONTEXT.battle_count % 2 == 1:
        slots_detect()
        will_unlock = CONTEXT.battle_count - _unlocked_slots + 1
        _unlocked_slots += 1
        if str(will_unlock) not in _empty_slots:
            click(_slot_pos[str(will_unlock)])
            if match(_buy_slot, False) is not None:
                click_until(False, _btn_buy_slot, _buy_slot)
            # else:
            #     # no coin or slot been covered
            #     return

    # buy
    for i in range(3):
        slots_detect()
        if len(_empty_slots) == 0:
            return
        j = len(_empty_slots)
        if goods_detect():
            for key in _red_goods:
                if j > 0:
                    j -= 1
                else:
                    break
                click(_goods_pos[key])
                click_until(False, match(_buy), _buy, 5)
        if i < 2 and j > 0:
            click(_btn_refresh)

    # fill slots
    slots_detect()
    _will_sale = _empty_slots
    for key in _goods_pos.keys():
        if len(_empty_slots) > 0:
            click(_goods_pos[key])
            click_until(False, match(_buy), _buy, 5)
            _empty_slots.pop()
        else:
            break


def run():
    log.info("enter node: store")
    if CONTEXT.battle_count == 0:
        log.debug("clear store context")
        global _red_goods
        global _will_sale
        global _empty_slots
        global _unlocked_slots
        _red_goods.clear()
        _will_sale.clear()
        _empty_slots.clear()
        _unlocked_slots = 0
    match(_store)
    sale_and_buy()
