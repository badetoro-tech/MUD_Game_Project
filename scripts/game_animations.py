import time
import sys
from font_format import format_font
import textwrap

DEFAULT_ANIMATION_TIME = 0.002
resource_folder = "../resources/"


def delay_print(chars, anim_time):
    if anim_time == 0:
        anim_time = DEFAULT_ANIMATION_TIME
    for char in chars:
        sys.stdout.write(format_font(char, 'fg', 'green'))
        sys.stdout.flush()
        time.sleep(anim_time)


def print_graphics(fn):
    graphics_path = resource_folder + fn
    with open(graphics_path, 'r') as animations_file:
        animations = animations_file.read()
    delay_print(animations, 0.002)


def wrap(string, max_width):
    return textwrap.fill(string, max_width)


class GameLoad:

    def __init__(self):
        pass
