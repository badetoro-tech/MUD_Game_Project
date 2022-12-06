import json
from font_format import format_font

monster_list_path = "../resources/monsters.json"
easy = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]


def load_monster_list():
    with open(monster_list_path, 'r') as monsters_file:
        monsters_dict = json.load(monsters_file)
    return monsters_dict


class Monsters:

    def __init__(self):
        self.species = ''
        self.attack = ''
        self.defense = ''
        self.health = ''
        self.monsters_dict = load_monster_list()

    def monster(self, species):
        self.species = species
        self.attack = self.monsters_dict[species]["attack"]
        self.defense = self.monsters_dict[species]["defense"]
        self.health = self.monsters_dict[species]["health"]


class Fight:

    def __init__(self):
        self.char_attack = 0
        self.char_health = 0
        self.monster_attack = 0
        self.monster_health = 0
        self.monster = Monsters()

    def check_for_monsters(self, current_location):
        # checking for goblins location
        for monster in self.monster.monsters_dict:
            # print(monster)
            # print(self.monster.monsters_dict[monster]["location"])
            if current_location in self.monster.monsters_dict[monster]["location"]:
                msg = f"You have just encountered a(n) {monster}"
                print(format_font(msg, 'bg', 'red'))
                return True
        return False

    def fight_monster(self, msg):
        pass




fg = Fight()
fg.check_for_monsters([4, 51])
