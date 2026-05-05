import os
import time

import cv2

from . import config
from .device import screenshot
from .logger import log

_BASE_DIR = os.path.dirname(__file__) + "\\..\\img\\"

# Templates: {path: (node, template, roi)}
_TEMPLATES: dict[str, tuple[str, cv2.typing.MatLike, list]] = {}

# _mask: str | None = None

_smart_timeout: dict[str, float] = {}


# def tmpl_load(path: str, roi: list):
def tmpl_load(node: str, template: dict[str, list]):
    path_list = list(template.keys())

    for path in path_list:

        if path in _TEMPLATES:
            raise ValueError(f"Template {path} already loaded.")

        roi = template[path]
        if roi is None:
            raise ValueError(f"Template {path} has no roi.")

        img = cv2.imread(_BASE_DIR + path)
        if img is None:
            raise FileNotFoundError(f"Template file {path} not found.")

        _TEMPLATES[path] = (node, img, roi)
        _smart_timeout[path] = config.DEFAULT_TIMEOUT

        log.debug(f"loaded template: {path}")


def tmpl_get(path: str) -> tuple[str, cv2.typing.MatLike, list]:
    if path not in _TEMPLATES:
        raise ValueError(f"Template {path} not loaded.")
    node, template, roi = _TEMPLATES[path]
    return node, template, roi


def tmpl_match(
    img, name: str, roi: list | None = None
) -> tuple[tuple[int, int], float]:
    """
    basic template matching, without smart_delay
    """
    start_time = time.time()
    # roi = [x, y, w, h]
    if roi is None:
        _, template, roi = tmpl_get(name)
    else:
        # roi override template
        _, template, _ = tmpl_get(name)

    # Get template dimensions for center calculation
    th, tw = template.shape[:2]

    # Crop image to ROI
    if img is None:
        raise ValueError("Image is None.")

    roi_img = img[roi[1] : roi[1] + roi[3], roi[0] : roi[0] + roi[2]]

    res = cv2.matchTemplate(roi_img, template, cv2.TM_CCOEFF_NORMED)  # type: ignore
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    # Calculate center:
    # (Top-left match in ROI) + (ROI offset) + (Half of template size)
    center_x = max_loc[0] + roi[0] + (tw // 2)
    center_y = max_loc[1] + roi[1] + (th // 2)

    # log.debug(f"matching {name} at ({center_x}, {center_y}), score: {max_val:.2f}")
    # if max_val < 0.7:
    #     cv2.imshow("roi", roi_img)
    #     cv2.waitKey(0)
    # log.debug(f"matching took {time.time() - start_time:.2f}s")

    return (center_x, center_y), max_val


def smart_delay(name: str, success=None):
    if success is None:
        time.sleep(_smart_timeout[name])
        return

    if success:
        delay = max(_smart_timeout[name] - 0.2, config.MIN_TIMEOUT)
    else:
        delay = min(_smart_timeout[name] + 0.2, config.MAX_TIMEOUT)

    log.debug(f"smart delay {name} {delay:.2f}s")
    _smart_timeout[name] = delay


def match(name: str, timeout: int | bool = 30) -> tuple[int, int] | None:
    """
    match with smart_delay and retry
    """
    # global _mask
    # if _mask is None:
    #     pass
    # elif _mask != name:
    #     log.debug(f"mask {_mask} mismatch {name}, abort")
    #     return None
    # else:
    #     log.debug(f"mask {_mask} match {name}, disable mask")
    #     _mask = None

    smart_delay(name)
    (x, y), score = tmpl_match(screenshot(), name)
    if score > 0.7:
        smart_delay(name, True)
        log.debug(f"match {name} at ({x}, {y}) success")
        return x, y
    else:
        smart_delay(name, False)
        log.debug(f"match {name} failed")

    if not timeout:
        log.info(f"retry is disable, give up")
        return None

    # give it a chance to recover
    log.error(f"match {name} timeout, retry")
    for _ in range(timeout):
        (x, y), score = tmpl_match(screenshot(), name)
        if score > 0.7:
            log.debug(f"match {name} at ({x}, {y}) success")
            return x, y

        time.sleep(1)

    # timeout
    if timeout >= 30:
        raise TimeoutError(name)

    return None

def match_all(img=None):
    """
    match all template
    """
    if img is None:
        img = screenshot()

    result = None
    max_score = 0
    for keys in _TEMPLATES.keys():
        (x, y), score = tmpl_match(
            img, keys, [0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT]
        )
        if score > 0.7:
            log.debug(f"match {keys} at ({x}, {y}), score: {score:.2f} success")
            if score > max_score:
                max_score = score
                # path, node
                result = keys, _TEMPLATES[keys][0]
        log.debug(f"match {keys}, score: {score:.2f}")
    log.debug(f"match all, result: {result}")
    return result
