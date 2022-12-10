import json
import random
import time
import matplotlib.pyplot as plt
from debug import print_debug
from game_animations import *
from monsters import *
from pprint import pprint
from scoring import top_scorers

GAME_MAP = "../resources/game_map.txt"
OBSTACLE = ["mountain", "valley", "lake", "wall", "old building"]
story = "../resources/story.txt"
monsters = Monsters()
fight = Fight()
control_directions = ['turn left', 'left', 'turn right', 'right', 'turn around', 'turn round', 'around', 'round']


def load_map():
    with open(GAME_MAP, 'r+') as f:
        # # read content from file and remove whitespaces around
        # content = f.read().strip()
        content = json.load(f)
        # # convert string format tuple to original tuple object (not possible using json.loads())
        # tuples = eval(content)
        # return tuples
    return content


def plot_map(char_location):
    g_map = load_map()
    x_array = []
    y_array = []
    for ls in g_map:
        x_array.append(ls[0])
        y_array.append(ls[1])

    plt.plot(x_array, y_array, label="Route", color='green', linestyle='dashed', linewidth=3)
    plt.plot(char_location[0], char_location[1], label="You", marker='o', markerfacecolor='blue', markersize=12)
    plt.show()


def load_story():
    with open(story, 'r+') as f:
        content = json.load(f)
    return content


def help_msg():
    print('The following are the possible controls you need to be aware of to play the game.')
    controls = '(Move) Forward\n(Turn) Left\n(Turn) Right\n(Turn) Round\nAttack\nHeal (Recover Health)' \
               '\nSave (To save your current game)\nLoad (To load your last saved game)\nCustomize (Character )' \
               '\nExit (To quit the game)' \
               '\nStatus (To view current Status)\nMap\nTop (See top 10 scores)\nHelp (To view controls again)\n'
    print(format_font(controls, 'fg', 'orange'))


def heal_character(character):
    view = [7, 11, 13, 17, 19, 23, 29]
    print(f'Your current health status is: '
          f'{character["data"]["health"][0]}/{character["data"]["health"][1]}')
    if {character["data"]["health"][0]} == {character["data"]["health"][1]}:
        print('You are already at maximum health.\n')
    else:
        confirm = input(wrap(format_font("Type 'heal' to confirm healing or any key to exit. Note that you cannot stop "
                                         "the healing process midway: ", "fg", "orange"), 100))
        confirm = confirm.lower()
        cnt = 0
        while character["data"]["health"][0] < character["data"]["health"][1] and character["data"]["health"][0] != 0:
            if confirm == 'heal':
                time.sleep(1.1)
                cnt += 1
                character["data"]["health"][0] += 1
                if cnt % random.choice(view) == 0:
                    print(f'You are recovering your heath. Current status is: '
                          f'{character["data"]["health"][0]}/{character["data"]["health"][1]}')
            else:
                break
        print(f'Your current health status is: '
              f'{character["data"]["health"][0]}/{character["data"]["health"][1]}\n')
    return character


class GamePlay:

    def __init__(self, character):
        self.character_update = None
        self.character = character
        self.orientation = 0
        self.face_direction = ''
        self.current_location = [0, 50]
        self.game_map = load_map()
        self.story = load_story()
        self.game_start_flag = 0

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
        self.character_orientation(1)
        return orientation

    def character_orientation(self, prn=0):
        if self.orientation == 0:
            direction = 'North'
        elif self.orientation == 90:
            direction = 'East'
        elif self.orientation == 180:
            direction = 'South'
        else:
            direction = 'West'
        self.face_direction = direction
        if prn == 1:
            print(f'You are now facing {direction}.')
        return direction

    def move_forward(self, orientation, current_location):
        x_loc = current_location[0]
        y_loc = current_location[1]
        if orientation == 0:
            y_loc += 1
        elif orientation == 180:
            y_loc += -1
        elif orientation == 90:
            x_loc += 1
        else:
            x_loc += -1
        new_location = [x_loc, y_loc]
        if new_location in load_map():
            self.current_location = new_location
            print(f"You move forward a few paces.")
            self.character['data']['steps'] += 1
            return self.current_location
        else:
            print(f"You cannot move forward because there is a {random.choice(OBSTACLE)} in front of you.")

        return self.current_location

    def start_game(self):
        self.orientation = self.character['data']['orientation']
        self.current_location = self.character['data']['location']
        if self.current_location == [0, 0]:
            msg = "\n\n ******* STARTING GAME *******"
            print(format_font(msg, 'fg', 'blue'))
            delay_print("LEGEND:\n*******\n", 0.025)
            delay_print(wrap(self.story["legend"], 100), 0.01)  # 0.025

            delay_print("\n\nTHE STORY:\n**********\n", 0.01)  # 0.025
            delay_print(wrap(self.story["intro"], 100), 0.01)  # 0.025
            print("\n")
            delay_print(wrap(self.story["game_start"], 100), 0.01)  # 0.025
            print("\n")
        else:
            print("Loading last save point...")

        # self.current_location = location
        if self.game_start_flag == 0:
            game_start_flag = 1
            help_msg()

        status = 'play'
        while status not in ('exit', 'save', 'load'):
            msg = 'Input your next action: '
            msg = msg.lower()
            g_play = input(format_font(msg, 'fg', 'orange'))
            rnd_choice = [0, 1, 2, 3, 4, 5]
            if g_play == 'exit':
                msg = input(wrap(format_font('Are you sure you want to exit? You will lose any unsaved progress. '
                                             'Type "exit to exit or press any other key to continue: ', 'fg', 'red'),
                                 100))
                if msg == 'exit':
                    status = msg
                    return [status, '']

            elif g_play == 'help':
                help_msg()

            elif g_play == 'heal':
                heal_character(self.character)

            elif g_play == 'move forward' or g_play == 'forward':
                self.move_forward(self.orientation, self.current_location)
                self.character['data']['location'] = self.current_location
                fight.check_for_boosters(self.character, self.current_location)
                check = fight.check_for_monsters(self.character, self.current_location)
                if check:
                    choice = input(format_font("Do you plan to attack or run. Type 'Attack' to attack or any "
                                               "key to run: ", 'fg', 'orange'))
                    if choice.lower() == 'attack':
                        fight.fight_monster(self.current_location, self.character)
                    else:
                        if random.choice(rnd_choice) <= 1:
                            print('You were able to escape.')
                        else:
                            print('The monster attacked before you were able to escape.')
                            fight.fight_monster(self.current_location, self.character)

            elif g_play in control_directions:
                if g_play == 'turn left' or g_play == 'left':
                    self.turn_direction(self.orientation, 'left')
                elif g_play == 'turn right' or g_play == 'right':
                    self.turn_direction(self.orientation, 'right')
                elif g_play == 'turn around' or g_play == 'turn round' or g_play == 'around' or g_play == 'round':
                    self.turn_direction(self.orientation, 'round')
                self.character['data']['orientation'] = self.orientation

            elif g_play == 'status':
                print('This is your current status:')
                print(f'Your name is: {self.character["data"]["char_name"]}')
                print(f'You are dressed in: {self.character["data"]["colour"]}')
                print(f'Your weapon of choice is: {self.character["data"]["weapon"]}')
                print(f'Your armour of choice is: {self.character["data"]["armour"]}')
                print(
                    f'Your heath status is: {self.character["data"]["health"][0]}/{self.character["data"]["health"][1]} (Current/Max)')
                print(f'Your attack power is : {self.character["data"]["attack power"]}')
                print(f'You are currently located in: {self.character["data"]["location"]}')
                print(f'You are currently facing: {self.character_orientation(0)}')
                print(f'You movement count: {self.character["data"]["steps"]}')
                print(f'Your score is currently: {self.character["data"]["score"]}\n')

            elif g_play == 'attack':
                print('There is nothing to attack.')

            elif g_play == 'map':
                plot_map(self.current_location)

            elif g_play == 'save':
                status = g_play
                return [status, self.character]

            elif g_play == 'load':
                status = g_play
                return [status, self.character]

            elif g_play == 'top':
                top_scorers()

            elif g_play == 'customize':
                self.customize_character()
                return ['save', self.character]

    def customize_character(self):
        """This method is used to customize the character after the initial customization"""
        print(format_font('You are about to customize your character.', 'fg', 'orange'))
        time.sleep(1)
        name_chk = input(f"Your Character's name is {format_font(self.character['data']['char_name'], 'fg', 'red')}. "
                         f"Would you like to change it? Type Y(es) or N(o)\n")
        if name_chk.lower() == 'y':
            self.character['data']['char_name'] = input(f"Enter your new name: \n")

        time.sleep(0.5)
        col_chk = input(f"Your Character's colour is {format_font(self.character['data']['colour'], 'fg', 'red')}. "
                        f"Would you like to change it? Type Y(es) or N(o)\n")
        if col_chk.lower() == 'y':
            self.character['data']['colour'] = input(f"Enter your new colour: \n")
