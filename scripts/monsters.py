import json
import random
import time
from debug import print_debug
from font_format import format_font

monster_list_path = "../resources/monsters.json"
attack_key = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
attack_strength = [2, 3, 4]


def load_monster_list():
    """
    Loads the monsters and booster list files
    :return: dictionary containing monsters and booster
    """
    with open(monster_list_path, 'r') as monsters_file:
        monsters_dict = json.load(monsters_file)
    return monsters_dict


def r_print(msg):
    """
    Using the font_format function, display messages in red
    :param msg: strings
    :return: red-coloured strings
    """
    print(format_font(msg, 'fg', 'red'))


def g_print(msg):
    """
    Using the font_format function, display messages in green
    :param msg: strings
    :return: green-coloured strings
    """
    print(format_font(msg, 'fg', 'green'))


def b_print(msg):
    """
    Using the font_format function, display messages in blue
    :param msg: strings
    :return: blue-coloured strings
    """
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
        # self.obj_location = []

    def check_for_monsters(self, character, current_location, prn=1):
        """
        This method is to check and confirm that a monster is located here current location
        :param character: The gamer's character
        :param current_location: Current location of the character
        :param prn: display print option
        :return: True if monster found, else False
        """
        for monster in self.monster.monsters_dict:
            if current_location in self.monster.monsters_dict[monster]["location"]:
                if current_location not in character['data']['expended_obj']:
                    if prn != 0:
                        msg = f"You have just encountered a(n) {monster}"
                        print(format_font(msg, 'bg', 'red'))
                    self.monster.species = monster
                    self.monster.monster(monster)
                    return True
        return False

    def fight_monster(self, current_location, character, prn=0):
        """
        This simulates a fight between the game character and the non-playable characters (NPC) in the game
        :param current_location: Current location of the character
        :param character: The gamer's character
        :param prn: display print option
        :return: True if monster found, else False
        """
        check_monster = self.check_for_monsters(character, current_location, prn)
        max_monster_health = self.monster.health
        if check_monster:
            end_fight = False
            while not end_fight:
                end_fight = self.fight_damage(character, self.monster.attack,
                                              self.monster.health, max_monster_health)
                pass

        return check_monster

    def fight_damage(self, character, m_attack, m_curr_health, m_max_health):
        """
        Calculate the damages of each of the two opponents attack
        :param character: The gamer's character
        :param m_attack: NPC attack strength
        :param m_curr_health: NPC current health
        :param m_max_health: NPC Maximum health
        :return: True if any character is killed, else False
        """
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
                character['data']['expended_obj'].append(character['data']['location'])
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
        """
        This method is to check and confirm that a booster is located here current location
        :param character: The gamer's character
        :param current_location: Current location of the character
        :param prn: display print option
        :return: True if booster found, else False
        """
        # checking for boosters' location
        print_debug('booster check entered', 5)
        print_debug(self.monster.boosters_dict, 5)
        for booster in self.monster.boosters_dict:
            if current_location in self.monster.boosters_dict[booster]["location"]:
                if current_location not in character['data']['expended_obj']:
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

                    character['data']['expended_obj'].append(character['data']['location'])

                return True
        return False
