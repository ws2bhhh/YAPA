import logging
import sys

from . import config

# 1. 定义颜色 ANSI 码
COLORS = {
    # "DEBUG": "\x1b[38;20m",  # 蓝色
    "DEBUG": "\x1b[44m",  # 蓝色
    "INFO": "\x1b[42m",  # 绿色
    "WARNING": "\x1b[43m",  # 黄色
    "ERROR": "\x1b[41m",  # 红色
    "CRITICAL": "\x1b[31m",  # 粗体红
    "RESET": "\x1b[0m",
}


def color_format(record):
    """动态添加颜色的函数"""
    levelname = record.levelname
    msg = record.msg

    # 获取对应颜色，如果没有则用默认
    color = COLORS.get(levelname, COLORS["RESET"])
    reset = COLORS["RESET"]

    record.levelname = f"{color}{levelname}{reset}"
    # record.msg = f"{color}{msg}{reset}"
    return True


# 2. 初始化单例 Logger
log = logging.getLogger()

if not log.handlers:
    log.setLevel(config.LOG_LEVEL)

    handler = logging.StreamHandler(sys.stdout)

    fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s] - %(message)s", datefmt="%H:%M:%S"
    )
    handler.setFormatter(fmt)

    handler.addFilter(color_format)

    log.addHandler(handler)
