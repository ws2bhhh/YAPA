import gzip
import io
import random
import subprocess
import time

import cv2
import numpy as np

from . import config
from .logger import log


def _set_serial(device_serial):
    config.SERIAL = device_serial


def _set_resolution():

    command = [
        "adb",
        "-s",
        config.SERIAL,
        "shell",
        "wm",
        "size",
        f"{config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}",
    ]
    subprocess.run(command)


def _init_scrcpy():

    command = ["scrcpy", "--serial", config.SERIAL, "-Sw", "--no-audio"]
    subprocess.Popen(command)


def connect(serial: str):
    if serial is None:
        raise ValueError("need device serial")
    _set_serial(serial)
    command = ["adb", "connect", config.SERIAL]
    subprocess.run(command)
    # _set_resolution()
    # _init_scrcpy()


def disconnect():
    command = ["adb", "-s", config.SERIAL, "shell", "wm", "size", "reset"]
    subprocess.run(command)
    subprocess.run(["adb", "disconnect"])


def screenshot():
    start_time = time.time()

    if config.SERIAL is None:
        raise ValueError("not initialized. Call set_device_serial first.")

    # 1. Capture and compress on-device, then pipe to stdout
    # We use 'sh -c' to allow piping inside the adb shell environment
    command = ["adb", "-s", config.SERIAL, "exec-out", "screencap -p | gzip"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the compressed bytes
    compressed_bytes, error = process.communicate()

    if error:
        # log.error(f"ADB Error: {error.decode().strip()}")
        raise Exception("ADB Error")

    # 2. Decompress the data in memory
    with gzip.GzipFile(fileobj=io.BytesIO(compressed_bytes)) as f:
        image_bytes = f.read()

    # 3. Convert raw bytes to a 1D numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # 4. Decode the PNG array into an OpenCV BGR image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 5. Log the time in milliseconds
    # log.debug(f"screenshot took {time.time() - start_time:.2f} ms")

    if img is None:
        raise Exception("screenshot failed")
    return img


def click(pos: tuple[int, int] | None):
    if pos is None:
        return

    x, y = pos

    start_time = time.time()
    if config.SERIAL is None:
        raise ValueError("not initialized. Call set_device_serial first.")

    # unknown bug fix
    # if offset:
    #     x -= config.X_OFFSET

    x += random.randrange(-5, 5)
    y += random.randrange(-5, 5)

    subprocess.run(
        ["adb", "-s", config.SERIAL, "shell", "input", "tap", str(x), str(y)]
    )
    log.debug(f"clicked at {x}, {y}")
    log.debug(f"click took {time.time() - start_time:.2f} ms")

