from pprint import pprint

DEBUG = 0


def print_debug(message, level):
    if level <= DEBUG:
        print("DEBUG:: ")
        pprint(message)
