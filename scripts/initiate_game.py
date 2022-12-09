from game_animations import print_graphics
from user_account import *
import time
import os
from debug import print_debug
from font_format import format_font

user_acct = UserAccount()
gd = "\n\nGame developed by:"
nm = "J. Adebayo Adetoro - 100394542."
dpt = "Department of Data Science."
sch = "University of East Anglia (UEA)."
cpr = "\xA92022. Version 1.0.\n"
welc = "Welcome to LIBERATING EARTH - THE SEARCH FOR THE LOST CITY OF ATLANTIS\n"


def initiate_game():
    if os.name == 'nt':
        os.system('cls')
        print_debug('The game is running on Windows OS', 6)
    else:
        os.system('clear')
        print_debug('The game is running on UNIX derivative OS', 6)

    print_graphics('intro_screen.txt')
    time.sleep(0.5)
    print(format_font(gd, 'fg', 'blue'))
    time.sleep(0.5)
    print(format_font(nm, 'fg', 'blue'))
    time.sleep(0.5)
    print(format_font(dpt, 'fg', 'blue'))
    time.sleep(0.5)
    print(format_font(sch, 'fg', 'blue'))
    time.sleep(0.5)
    print(format_font(cpr, 'ef', 'blue'))
    time.sleep(1.0)
    print(format_font(welc, 'fg', 'red'))
    time.sleep(0.5)
    start_game()


def start_game():
    check_for_account_profile_file()
    check_for_top_scorers_file()
    check_for_user_char_file()
    game_state = True
    while game_state:
        print("You will need to have an account to play the game.")
        print(f"If you are a new player, type {format_font('N', 'fg', 'red')} and press enter")
        print(f"If you already have an account, type {format_font('L', 'fg', 'red')} to login and continue from where "
              f"you stopped")
        g_start = input(f"Otherwise, type {format_font('EXIT', 'fg', 'red')} and press enter, to exit the game:\n")
        while g_start.lower() not in ('n', 'l', 'exit'):
            g_start = input(f"You have entered the wrong input. Try again or type {format_font('EXIT', 'fg', 'red')} "
                            f"to exit the game\n")
        if g_start.lower() == 'n':
            print("You are about to create your account...")
            user_acct.enter_username()
            check_acct_avail = user_acct.check_if_account_exists('n')
            while check_acct_avail:
                check_acct_avail = user_acct.check_if_account_exists('n')
            user_acct.create_user()
            game_state = user_acct.load_user()
            # return game_state
            break

        elif g_start.lower() == "l":
            print("You will be required to enter your USER ACCOUNT name...")
            user_acct.enter_username()
            check_acct_avail = user_acct.check_if_account_exists('l')
            while check_acct_avail[0] and check_acct_avail[1] != 'exit':
                check_acct_avail = user_acct.check_if_account_exists('l')
                print_debug(f'***********: {check_acct_avail}', 3)
            if check_acct_avail[1] != 'exit':
                user_acct.load_user()
            print('\n\n')

        elif g_start.lower() == "exit":
            print("We are sorry to see you go. Exiting the game ...")
            break
