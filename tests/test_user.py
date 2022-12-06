import unittest

from scripts.user_account import *
from scripts.game_play import *
from scripts.monsters import *


class TestUser(unittest.TestCase):
    def setUp(self):
        """Initiate parameters for unit testing"""
        self.user = UserAccount()
        self.gameplay = GamePlay()
        self.monsters = Monsters()
        self.fight_monster = Fight()
        self.user.username = 'testuser'
        self.user.password = 'password'
        self.user.hashed_password = '6d746f5e7c4cfb1583e9ca5050daa8b7fe4badbbb5ae7ff3fcf022487166f8da'


class TestGamePlay(TestUser):
    def test_turn_left(self):
        """Test to ensure that the gamer character face the correct direction when turning left"""
        self.assertEqual(self.gameplay.turn_direction(0, 'right'), 90)
        self.assertEqual(self.gameplay.turn_direction(90, 'right'), 180)
        self.assertEqual(self.gameplay.turn_direction(180, 'right'), 270)
        self.assertEqual(self.gameplay.turn_direction(270, 'right'), 0)

    def test_turn_round(self):
        """Test to ensure that the gamer character face the correct direction when turning round"""
        self.assertEqual(self.gameplay.turn_direction(0, 'round'), 180)
        self.assertEqual(self.gameplay.turn_direction(90, 'round'), 270)
        self.assertEqual(self.gameplay.turn_direction(180, 'round'), 0)
        self.assertEqual(self.gameplay.turn_direction(270, 'round'), 90)

    def test_turn_right(self):
        """Test to ensure that the gamer character face the correct direction when turning right"""
        self.assertEqual(self.gameplay.turn_direction(0, 'left'), 270)
        self.assertEqual(self.gameplay.turn_direction(90, 'left'), 0)
        self.assertEqual(self.gameplay.turn_direction(180, 'left'), 90)
        self.assertEqual(self.gameplay.turn_direction(270, 'left'), 180)

    def test_move_forward_at_beginning(self):
        """Test to ensure the character can move forward at the beginning"""
        self.assertEqual(self.gameplay.move_forward(self.gameplay.orientation, self.gameplay.current_location), [1, 50])

    def test_move_forward_after_left_turn(self):
        """Test to ensure the character cannot turn left and move forward at the beginning"""
        self.gameplay.turn_direction(0, 'left')
        self.assertEqual(self.gameplay.move_forward(self.gameplay.orientation, self.gameplay.current_location), [0, 50])

    def test_move_forward_after_round_turn(self):
        """Test to ensure the character cannot turn round and move forward at the beginning"""
        self.gameplay.turn_direction(90, 'round')
        self.assertEqual(self.gameplay.move_forward(self.gameplay.orientation, self.gameplay.current_location), [0, 50])

    def test_move_forward_then_turn(self):
        """Test to ensure the character move foreward 4 times before turning """
        self.gameplay.move_forward(self.gameplay.orientation, self.gameplay.current_location)
        self.gameplay.move_forward(self.gameplay.orientation, self.gameplay.current_location)
        self.gameplay.move_forward(self.gameplay.orientation, self.gameplay.current_location)
        self.gameplay.move_forward(self.gameplay.orientation, self.gameplay.current_location)
        self.gameplay.turn_direction(0, 'right')
        self.assertEqual(self.gameplay.move_forward(self.gameplay.orientation, self.gameplay.current_location), [4, 51])

    def test_orientation_to_north(self):
        """Test to check the starting character orientation"""
        self.assertEqual(self.gameplay.orientation, 0)

    def test_direction_north(self):
        self.assertEqual(self.gameplay.character_orientation(), 'North')

    def test_direction_east(self):
        self.gameplay.turn_direction(0, 'right')
        self.assertEqual(self.gameplay.character_orientation(), 'East')

    def test_direction_south(self):
        self.gameplay.turn_direction(0, 'round')
        self.assertEqual(self.gameplay.character_orientation(), 'South')

    def test_direction_west(self):
        self.gameplay.turn_direction(0, 'left')
        self.assertEqual(self.gameplay.character_orientation(), 'West')


class TestPasswordHash(TestUser):
    def test_password_hash(self):
        """Test to ensure the password hashing is working as it should"""
        self.assertEqual(self.user.hash_password(self.user.password), self.user.hashed_password)

    def test_validate_correct_password(self):
        """Test to ensure that the checking of hashed password against encrypted password works"""
        self.assertEqual(self.user.check_password(self.user.hashed_password), True)

    def test_validate_wrong_password(self):
        """Test to ensure that the checking of plain-text password against encrypted password fails"""
        self.test_password_hash()
        self.assertEqual(self.user.check_password(self.user.password), False)


class TestMonsters(TestUser):
    def test_monster_orc_attack(self):
        self.monsters.monster("orc")
        self.assertEqual(self.monsters.attack, 8)

    def test_monster_orc_defense(self):
        self.monsters.monster("orc")
        self.assertEqual(self.monsters.defense, 6)

    def test_monster_orc_health(self):
        self.monsters.monster("orc")
        self.assertEqual(self.monsters.health, 70)

    def test_confirm_monster_location(self):
        self.assertEqual(self.fight_monster.check_for_monsters([4, 51]), True)

    def test_confirm_monster_location_invalid(self):
        self.assertEqual(self.fight_monster.check_for_monsters([0, 50]), False)


if __name__ == '__main__':
    unittest.main()
