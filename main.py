from action import *
from utils import device
from utils.img_match import match_all
from utils.logger import log

# change to your emulator serial.
# example:
# DEVICE = "emulator-5555"
# DEVICE = "127.0.0.1:16384"

DEVICE = 

device.connect(DEVICE)
ACTS = [
    game_start,
    gift,
    # task,
    skill_select,
    store,
    battle_start,
    battle_wait,
    game_over,
]
NODE_TO_ACTS = {
    "game_start": 0,
    "gift": 1,
    # "task": 2,
    "skill_select": 2,
    "store": 3,
    "battle": 4,
    "battle_wait": 5,
    "game_over": 6,
}
target_index = 0


while True:
    try:
        for i in range(len(ACTS)):
            if i >= target_index:
                ACTS[i].run()
                target_index = 0
    except TimeoutError:
        target_index = relocate.run(NODE_TO_ACTS)
        if target_index is None:
            exit()
