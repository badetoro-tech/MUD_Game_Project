import time
import sys
from font_format import format_font  # Used to format texts with colours
import textwrap

DEFAULT_ANIMATION_TIME = 0.002
resource_folder = "../resources/"


def delay_print(chars, delay_time):
    """
    This is used to generate an ascii text animation by printing a string of texts one character at a time
    :param chars: The characters or string you want to animate
    :param delay_time: The delay time within each character in secs
    :return:
    """
    if delay_time == 0:
        delay_time = DEFAULT_ANIMATION_TIME
    for char in chars:
        sys.stdout.write(format_font(char, 'fg', 'green'))
        sys.stdout.flush()
        time.sleep(delay_time)


def print_graphics(fn):
    """
    This function is used to load files and print contents one at a time using the delay_print function
    :param fn: This is the file name
    :return:
    """
    graphics_path = resource_folder + fn
    with open(graphics_path, 'r') as animations_file:
        animations = animations_file.read()
    delay_print(animations, 0.002)


def wrap(string, max_width):
    """This function is used to wrap text so that it does not print off-screen. It accepts the following parameters:
        :param string: The text that needed wrapping
        :param max_width: the maximum length of texts of the string before wrapping is enforced
        :return:
    """
    return textwrap.fill(string, max_width)

# class GameLoad:
#
#     def __init__(self):
#         pass
