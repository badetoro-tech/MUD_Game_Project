import json
import random
from debug import print_debug
# from user_account import *
from game_animations import *

GAME_MAP = "../resources/game_map.txt"
OBSTACLE = ["mountain", "valley", "lake", "wall", "old building"]
story = "../resources/story.txt"


def load_map():
    with open(GAME_MAP, 'r+') as f:
        # # read content from file and remove whitespaces around
        # content = f.read().strip()
        content = json.load(f)
        # # convert string format tuple to original tuple object (not possible using json.loads())
        # tuples = eval(content)
        # return tuples
    return content


def load_story():
    with open(story, 'r+') as f:
        content = json.load(f)
    return content


class GamePlay:

    def __init__(self):
        self.orientation = 0
        self.current_location = [0, 50]
        self.game_map = load_map()
        self.story = load_story()

    def turn_direction(self, orientation, direction):
        print_debug(f'Old Orientation: {orientation}', 4)
        if direction == 'right':
            orientation = (orientation + 90) % 360
        elif direction == 'left':
            orientation = (orientation + 270) % 360
        elif direction in ['round', 'around']:
            orientation = (orientation + 180) % 360
        self.orientation = orientation
        print_debug(f'New Orientation after turning {direction}: {self.orientation}', 4)
        self.character_orientation()
        return orientation

    def character_orientation(self):
        if self.orientation == 0:
            direction = 'North'
        elif self.orientation == 90:
            direction = 'East'
        elif self.orientation == 180:
            direction = 'South'
        else:
            direction = 'West'
        print(f'You are now facing {direction}.')
        return direction

    def move_forward(self, orientation, current_location):
        x_loc = current_location[0]
        y_loc = current_location[1]
        if orientation == 0:
            x_loc += 1
        elif orientation == 180:
            x_loc += -1
        elif orientation == 90:
            y_loc += 1
        else:
            y_loc += -1
        new_location = [x_loc, y_loc]
        if new_location in load_map():
            self.current_location = new_location
            return self.current_location
        else:
            print(f"You cannot move forward because there is a {random.choice(OBSTACLE)} in front of you.")
        return self.current_location

    def start_game(self, location, orientation):
        if location == [0, 50]:
            msg = "\n\n ******* STARTING GAME *******"
            print(format_font(msg, 'fg', 'blue'))
            delay_print("LEGEND:\n*******\n", 0.025)
            delay_print(wrap(self.story["legend"], 100), 0.025)

            delay_print("\n\nTHE STORY:\n**********\n", 0.025)
            delay_print(wrap(self.story["intro"], 100), 0.025)
            print("\n")
            delay_print(wrap(self.story["game_start"], 100), 0.025)
            print("\n")
        else:
            print("loading last save point")

        self.current_location = location
        print('The following are the possible controls you need to be aware of to play the game.')
        controls = '(Move )forward\n(Turn )Left\n(Turn )Right\n(Turn )Round\nAttack\nSave (To save your current game)' \
                   '\nExit (To quit the game)\nStatus (To view current Status)\nHelp (To view controls again)\n'
        print(format_font(controls, 'fg', 'orange'))

        status = 'play'
        while status != 'exit':
            msg = 'Input your next action: '
            msg = msg.lower()
            g_play = input(format_font(msg, 'fg', 'orange'))
            if g_play == 'exit':
                msg = input(format_font('Are you sure you want to exit? You will lose any unsaved progress. '
                                        'Type "exit to exit or press any other key to continue. ', 'fg', 'red'))
                if msg == 'exit':
                    break
            elif g_play == 'move forward' or g_play == 'forward':
                self.move_forward(self.orientation, self.current_location)
            elif g_play == 'turn left' or g_play == 'left':
                self.turn_direction(self.orientation, 'left')
            elif g_play == 'turn right' or g_play == 'right':
                self.turn_direction(self.orientation, 'right')
            elif g_play == 'turn around' or g_play == 'turn round' or g_play == 'around' or g_play == 'round':
                self.turn_direction(self.orientation, 'round')
