import json
import random
import time
from debug import print_debug

from font_format import format_font

monster_list_path = "../resources/monsters.json"
attack_key = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
attack_strength = [2, 3, 4]


def load_monster_list():
    with open(monster_list_path, 'r') as monsters_file:
        monsters_dict = json.load(monsters_file)
    return monsters_dict


def r_print(msg):
    print(format_font(msg, 'fg', 'red'))


def g_print(msg):
    print(format_font(msg, 'fg', 'green'))


def p_print(msg):
    print(format_font(msg, 'fg', 'purple'))


def b_print(msg):
    print(format_font(msg, 'fg', 'blue'))


class Monsters:

    def __init__(self):
        self.species = ''
        self.attack = ''
        self.defence = ''
        self.health = ''
        self.load_monster = load_monster_list()
        self.monsters_dict = self.load_monster[0]
        self.boosters_dict = self.load_monster[1]
        self.booster_val = 0

    def monster(self, species):
        self.species = species
        self.attack = self.monsters_dict[species]["attack"]
        self.defence = self.monsters_dict[species]["defence"]
        self.health = self.monsters_dict[species]["health"]


class Fight:

    def __init__(self):
        self.char_attack = 0
        self.char_health = 0
        # self.monster_attack = 0
        # self.monster_health = 0
        self.monster = Monsters()
        # self.meet_monster = ''

    def check_for_monsters(self, current_location, prn=1):
        # checking for monster's location
        for monster in self.monster.monsters_dict:
            if current_location in self.monster.monsters_dict[monster]["location"]:
                if prn != 0:
                    msg = f"You have just encountered a(n) {monster}"
                    print(format_font(msg, 'bg', 'red'))
                    self.monster.species = monster
                    self.monster.monster(monster)
                return True
        return False

    def fight_monster(self, current_location, character, prn=0):
        check_monster = self.check_for_monsters(current_location, prn)
        max_monster_health = self.monster.health
        if check_monster:
            end_fight = False
            while not end_fight:
                end_fight = self.fight_damage(character, self.monster.attack,
                                              self.monster.health, max_monster_health)
                pass

        return check_monster

    def fight_damage(self, character, m_attack, m_curr_health, m_max_health):
        attacking = random.choice(attack_key)
        time.sleep(1)
        if attacking == 1:
            att_str = int(character['data']['attack power'] / random.choice(attack_strength))
            character['data']['score'] += (att_str * 20)  # Keeping Scores
            if int(m_curr_health) - att_str < 0:
                self.monster.health = 0
            else:
                self.monster.health = int(m_curr_health) - att_str
            # monster_health = [self.monster.health, m_max_health]
            g_print(f'You were able to hit the {self.monster.species} for {att_str} damage. The monster now have '
                    f'{self.monster.health}/{m_max_health} health.')
            if self.monster.health <= 0:
                b_print(f'You have successfully defeated the {self.monster.species}.')
                return True
        else:
            g_print(f'Your attack missed the {self.monster.species}. The monster still has '
                    f'{m_curr_health}/{m_max_health} health.')

        time.sleep(1)
        defending = random.choice(attack_key)
        if defending == 0:
            def_str = int(m_attack / (random.choice(attack_strength)))
            character['data']['score'] -= (def_str * 5)  # Keeping Scores
            if (character['data']['health'][0] - def_str) < 0:
                character['data']['health'][0] = 0
            else:
                character['data']['health'][0] -= def_str
            g_print(f"The {self.monster.species} was able to attack you for {def_str} damage. You now have "
                    f"{character['data']['health'][0]}/{character['data']['health'][1]} health.")
            if character['data']['health'][0] <= 0:
                r_print(f'Your character has been defeated by the {self.monster.species}.')
                return True
        else:
            g_print(f"You were able to defend against the {self.monster.species}. You still have  "
                    f"{character['data']['health'][0]}/{character['data']['health'][1]} health.")
        return False

    def check_for_boosters(self, character, current_location, prn=1):
        # checking for boosters' location
        print_debug('booster check entered', 5)
        print_debug(self.monster.boosters_dict, 5)
        for booster in self.monster.boosters_dict:
            if current_location in self.monster.boosters_dict[booster]["location"]:
                if prn != 0:
                    msg = f"You have just picked up a booster pack: {booster}"
                    print(format_font(msg, 'bg', 'red'))
                if booster.lower() == "health pack":
                    print_debug('Getting a health pack', 5)
                    character['data']['health_booster'] += int(self.monster.boosters_dict[booster]["boost"])
                    character['data']['health'][1] += int(self.monster.boosters_dict[booster]["boost"])
                    character['data']['health'][0] = character['data']['health'][1]
                    msg = f"Your health has been restored to a maximum value of {character['data']['health'][1]}"
                    print(format_font(msg, 'bg', 'red'))

                if booster.lower() == "weapon magazines":
                    print_debug('Getting a weapon magazines', 5)
                    character['data']['attack_booster'] += int(self.monster.boosters_dict[booster]["boost"])
                    character['data']['attack power'] += int(self.monster.boosters_dict[booster]["boost"])
                    msg = f"Your attack power has been increased by {self.monster.boosters_dict[booster]['boost']}"
                    print(format_font(msg, 'bg', 'red'))

                return True
        return False
