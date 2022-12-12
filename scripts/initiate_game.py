from game_animations import print_graphics
from user_account import *
import time
import os
from debug import print_debug  # Used to generate debug information for further code analysis
from font_format import format_font  # Used to format texts with colours

user_acct = UserAccount()  # Load UserAccount class from user_account
gd = "\n\nGame developed by:"
nm = "J. Adebayo Adetoro - 100394542."
dpt = "Department of Data Science."
sch = "University of East Anglia (UEA)."
cpr = "\xA92022. Version 1.0.\n"
welcome_greetings = "Welcome to LIBERATING EARTH - THE SEARCH FOR THE LOST CITY OF ATLANTIS\n"


def initiate_game():
    """This function is to initialise the game. It accepts no arguments"""
    # Checking to clear the command prompt in order to support both Windows and Unix-derivative OS
    if os.name == 'nt':
        os.system('cls')
        print_debug('The game is running on Windows OS', 6)
    else:
        os.system('clear')
        print_debug('The game is running on UNIX derivative OS', 6)

    # Begin Game intro animation
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
    print(format_font(welcome_greetings, 'fg', 'red'))
    time.sleep(0.5)
    # Calling the start_game() function
    start_game()


def start_game():
    """This function starts the game proper after the introduction. It accepts no arguments"""
    check_for_account_profile_file()  # Check to confirm and create account profile file if not found
    check_for_top_scorers_file()  # Check to confirm and create the top scores' file if not found
    check_for_user_char_file()  # Check to confirm and create user character customisation file if not found

    # Initialise game_state as True (i.e. running)
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
            # Enter Username
            user_acct.enter_username()
            # Check if the username entered above exist before processing further
            check_acct_avail = user_acct.check_if_account_exists('n')
            while check_acct_avail[0]:
                check_acct_avail = user_acct.check_if_account_exists('n')
            # Create the user if the username does not exist
            user_acct.create_user()
            # Load the user account
            user_acct.load_user()
            break

        elif g_start.lower() == "l":
            print("You will be required to enter your USER ACCOUNT name...")
            # Enter Username
            user_acct.enter_username()
            # Check if the username entered above exist before processing further
            check_acct_avail = user_acct.check_if_account_exists('l')
            while check_acct_avail[0] and check_acct_avail[1] != 'exit':
                check_acct_avail = user_acct.check_if_account_exists('l')
                print_debug(f'***********: {check_acct_avail}', 3)
            # Load user if the gamer is not exiting the game
            if check_acct_avail[1] != 'exit':
                user_acct.load_user()
            print('\n\n')

        # Exit the game if the user entered the option
        elif g_start.lower() == "exit":
            print("We are sorry to see you go. Exiting the game ...")
            break
