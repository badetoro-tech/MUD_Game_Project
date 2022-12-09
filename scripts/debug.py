from pprint import pprint

DEBUG = 0


def print_debug(message, level):
    if level <= DEBUG:
        print(f"DEBUG:: {message}")
        # pprint(message)
