from json import JSONDecodeError
from pathlib import Path
import pandas as pd
import csv
import hashlib  # , uuid
from debug import print_debug
from sty import fg
import json
from pprint import pprint
from font_format import format_font
from game_play import GamePlay
from getpass import getpass
import time
from scoring import *

USER_PROFILE_FILE = "../resources/user_accounts.csv"
TOP_SCORERS_FILE = "../resources/top_scorers.csv"
USER_CHARACTERS_FILE = "../resources/user_characters.json"
SALT = 'abfdee2d837a4be79f7cdbcd3c2b76b0'  # uuid.uuid4().hex
WEAPONS = "../resources/weapons.json"


def check_for_account_profile_file():
    path = Path(USER_PROFILE_FILE)
    # if account profile file does not exist, create the new account
    if not path.is_file():
        with open(USER_PROFILE_FILE, 'w', newline='') as file:
            # create a csvwriter object
            print_debug(f'The account profile file does not exist. Creating the file in path: {USER_PROFILE_FILE}', 2)
            csvwriter = csv.writer(file)
            # write the header row
            header = ['username', 'password']
            csvwriter.writerow(header)


def check_for_top_scorers_file():
    path = Path(TOP_SCORERS_FILE)
    # if account profile file does not exist, create the new account
    if not path.is_file():
        with open(TOP_SCORERS_FILE, 'w', newline='') as file:
            # create a csvwriter object
            print_debug(f'The top scorer file does not exist. Creating the file in path: {TOP_SCORERS_FILE}', 2)
            csvwriter = csv.writer(file)
            # write the header row
            header = ['Position', 'Username', 'Character Name', 'Points']
            csvwriter.writerow(header)


def check_for_user_char_file():
    path = Path(USER_CHARACTERS_FILE)
    # if user character files does not exist, create a new file
    if not path.is_file():
        with open(USER_CHARACTERS_FILE, 'w', newline='') as file:
            game_characters = []
            print_debug(f'The user character file does not exist. Creating the file in path: {USER_CHARACTERS_FILE}', 2)
            file.write(str(game_characters))


class UserAccount:

    def __init__(self):
        self.username = ''
        # self.password = ''
        self.hashed_password = ''
        self.red_username = fg.red + self.username + fg.rs
        self.character = {}
        self.char_name = ''
        self.colour = ''
        self.data = []
        self.weapons_dict = {}
        self.score = 0
        # self.sc = ScoreBoard()

    def hash_password(self, password):
        print_debug(f'The plaintext password is: {password}', 2)
        self.hashed_password = hashlib.sha256(str(self.username + password + SALT).encode('utf-8')).hexdigest()
        print_debug(f'The hashed password is: {self.hashed_password}', 2)
        return self.hashed_password

    def validate_password(self, hashed_pass):
        if self.hashed_password == hashed_pass:
            print('Your password has been validated successfully')
            return True
        else:
            print('You entered the wrong password!')
            return False

    def enter_username(self):
        # print_debug(f"User account input in enter_username() is: {user_acct_input}", 3)
        user_acct_input = ''
        cnt = 0
        while len(user_acct_input) < 4:
            if cnt > 0:
                print("Your ACCOUNT name did not meet the minimum requirements.")
            user_acct_input = input("Enter the name of your ACCOUNT (minimum of 4 characters):\n")
            cnt += 1
        # if user_acct_input.lower() == 'exit':
        #     return user_acct_input.lower()
        self.username = user_acct_input.lower()
        return self.username

    def enter_password(self):
        pass_input = ''
        while len(pass_input) < 4:
            try:
                pass_input = getpass('Enter your account password (minimum of 4 characters): \n')
            except:
                pass_input = input('Enter your account password (minimum of 4 characters): \n')

        self.hashed_password = self.hash_password(pass_input)
        return self.hashed_password

    def create_user(self):
        hashed_pass = self.enter_password()
        user_data = [self.username, hashed_pass]
        print_debug(f'The username and hashed password is: {user_data}', 2)
        with open(USER_PROFILE_FILE, 'a', newline='') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(user_data)
        print(f"Player Account {self.red_username} has been created successfully.")

    def check_if_account_exists(self, load_state):
        content = pd.read_csv(USER_PROFILE_FILE)
        usernames = content.username.tolist()
        passwords = content.password.tolist()
        print_debug(f"Viewing the usernames available in the user profiles file:", 4)
        print_debug(f"{usernames}", 4)
        if self.username in usernames and load_state == 'n':
            print(f"Player Account {fg.red + self.username + fg.rs} already exists. Type in another username "
                  f"or {fg.red + 'exit' + fg.rs} to go to the previous menu.")
            username = self.enter_username()
            return [True, username]
        elif self.username not in usernames and load_state == 'l':
            print(f"Player Account {fg.red + self.username + fg.rs} does not exist. Type in the correct username "
                  f"or {fg.red + 'exit' + fg.rs} to go to the previous menu.")
            username = self.enter_username()
            return [True, username]
        elif self.username in usernames and load_state == 'l':
            pwd_check_success = False
            while not pwd_check_success:
                self.enter_password()
                hashed_pwd = passwords[usernames.index(self.username)]
                pwd_check_success = self.validate_password(hashed_pwd)

        return [False, '']

    def load_user(self):

        game_status = {}
        print(f"Loading user character...")
        self.user_characters()
        print(f'Loading Game...')
        print_debug(self.character, 5)
        print_debug(f"location: {self.character['data']['location']}", 5)
        gp = GamePlay(self.character)
        play_game = True
        while play_game:
            game_status = gp.start_game()
            if game_status[0] == 'exit':
                play_game = False
                print('Exiting...')
                return play_game
            elif game_status[0] == 'save':
                print('Saving Game ...')
                self.save_game_data(game_status[1])
                print('Save Successful...')
            elif game_status[0] == 'load':
                self.load_user()

        return play_game

    def user_characters(self):
        game_data = self.load_game_data()
        print_debug(f'Game Data: {game_data}', 5)
        [print_debug(d['username'], 5) for d in game_data]
        gamer_data = {}
        username_found = False
        for x in game_data:
            # pprint(x)
            if self.username == x['username']:
                username_found = True
                gamer_data = x
                break

        if not username_found:
            print('You character has not been created yet. You need to create one....')
            self.character = self.initiate_characters()
            self.customize_character()

        else:
            print('Character found.')
            self.character = gamer_data

    def initiate_characters(self):
        player_character = {"username": self.username,
                            "data": {
                                "char_name": "",
                                "colour": "",
                                "health": [100, 100],
                                "attack power": 5,
                                "weapon": "",
                                "weapon_att": 0,
                                "weapon_def": 0,
                                "armour": "",
                                "armour_att": 0,
                                "armour_def": 0,
                                "location": [0, 0],
                                "orientation": 0,
                                "health_booster": 0,
                                "attack_booster": 0,
                                "defence_booster": 0,
                                "steps": 0,
                                "score": 0},
                            }
        return player_character

    def customize_character(self):
        """This is used to customize your character at the beginning of the game"""
        self.char_name = input('Enter your character name:\n')
        self.colour = input('Customize your character by selecting color of outfit:\n')
        self.character['data']['char_name'] = self.char_name
        self.character['data']['colour'] = self.colour
        weapon_check = True
        armour_check = True
        while weapon_check:
            with open(WEAPONS, 'r') as weapon_file:
                print("You need to select a weapon. The following weapons are available: ")
                self.weapons_dict = json.load(weapon_file)
                # pprint(self.weapons_dict)
                weapon_list = []
                weapon_att_list = []
                weapon_def_list = []
                for d in self.weapons_dict[0]:
                    weapon_att = self.weapons_dict[0][d]['attack']
                    weapon_def = self.weapons_dict[0][d]['defence']
                    weapon_list.append(d)
                    weapon_att_list.append(weapon_att)
                    weapon_def_list.append(weapon_def)
                    print(f"{format_font(d, 'fg', 'green')} => "
                          f"Attack Power: {format_font(str(weapon_att), 'fg', 'red')}, "
                          f"defence Power: {format_font(str(weapon_def), 'fg', 'red')}")
                v_weapon = input("Select your weapon by typing the weapon name below:\n")
                if v_weapon in weapon_list:
                    idx = weapon_list.index(v_weapon)
                    print_debug(f'INDEX POSITION: {idx}', 7)
                    weapon_att = weapon_att_list[idx]
                    weapon_def = weapon_def_list[idx]
                    print_debug(f'weapon_att : {weapon_att}', 5)
                    print(f"You have selected a {format_font(str(v_weapon), 'fg', 'red')} as your weapon.")
                    self.character['data']['weapon'] = v_weapon
                    self.character['data']['weapon_att'] = weapon_att
                    self.character['data']['weapon_def'] = weapon_def
                    weapon_check = False
                    # break
                else:
                    print("You did not select a valid weapon. Try again.")

        while armour_check:
            with open(WEAPONS, 'r') as weapon_file:
                print("You need to select an armour. The following armours are available: ")
                self.weapons_dict = json.load(weapon_file)
                armour_list = []
                armour_att_list = []
                armour_def_list = []
                for d in self.weapons_dict[1]:
                    armour_att = self.weapons_dict[1][d]['attack']
                    armour_def = self.weapons_dict[1][d]['defence']
                    armour_list.append(d)
                    armour_att_list.append(weapon_att)
                    armour_def_list.append(weapon_def)
                    print(f"{format_font(d, 'fg', 'green')} => "
                          f"Attack Power: {format_font(str(armour_att), 'fg', 'red')}, "
                          f"defence Power: {format_font(str(armour_def), 'fg', 'red')}")
                v_armour = input("Select your armour by typing the armour name below:\n")
                if v_armour in armour_list:
                    idx = armour_list.index(v_armour)
                    print_debug(f'INDEX POSITION: {idx}', 7)
                    armour_att = armour_att_list[idx]
                    armour_def = armour_def_list[idx]
                    print_debug(f'armour_att : {armour_att}', 5)
                    print(f"You have selected a {format_font(str(v_armour), 'fg', 'red')} as your armour.")
                    self.character['data']['armour'] = v_armour
                    self.character['data']['armour_att'] = armour_att
                    self.character['data']['armour_def'] = armour_def
                    # self.update_character()
                    armour_check = False
                else:
                    print("You did not select a valid armour. Try again.")

        self.update_character()

    def update_character(self):
        print('Updating the character customisation.')
        v_cur_health = self.character['data']['health'][0] - self.character['data']['health'][1] + 100
        v_cur_health += (self.character['data']['weapon_def'] * 5) + (self.character['data']['armour_def'] * 5)
        v_cur_health += self.character['data']['health_booster'] + (self.character['data']['defence_booster'] * 5)

        v_max_health = 100 + (self.character['data']['weapon_def'] * 5) + (self.character['data']['armour_def'] * 5)
        v_max_health += self.character['data']['health_booster'] + (self.character['data']['defence_booster'] * 5)

        v_attack_pow = 5 + self.character['data']['weapon_att'] + self.character['data']['armour_att']

        self.character['data']['health'] = [v_cur_health, v_max_health]
        self.character['data']['attack power'] = v_attack_pow

        self.save_game_data(self.character)

    def load_game_data(self):
        try:
            with open(USER_CHARACTERS_FILE, 'r') as file:
                self.data = json.load(file)
        except JSONDecodeError:
            self.data = []
        return self.data

    def save_game_data(self, character):
        # pprint(character)
        # pprint(self.data)

        # Save the data back into the user_accounts.csv
        if not self.data:
            self.data.append(character)
        else:
            for char_dict in self.data:
                # print('************************')
                # print(char_dict)
                # print(char_dict['username'])
                if char_dict['username'] == character['username']:
                    idx = self.data.index(char_dict)
                    self.data[idx] = character
            # print('^^^^^^^^^^^^^^^^^^^^^^^^')
            # pprint(self.data)
        with open(USER_CHARACTERS_FILE, "w") as outfile:
            json.dump(self.data, outfile)

        # Update the scores table
        ScoreBoard(character['data']['score'], character['username'], character['data']['char_name'])

        time.sleep(2)
