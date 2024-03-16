import io
import sys
import time
from game_manager import GameManager

# Provides the user a list of options at the beginning of the game
def GettingStarted():
    while True:
        print("Welcome to Connect 4.")
        print("1. Read the rules ")
        print("2. Play Game")
        print("3. Quit")

        option = input("What would you like to do? ")

        print()

        if IsValidOption(option, [1, 2, 3]):
            option = int(option)
            break

    return option

# Reads the rules from an external file and presents it to the player
def Rules():
    pass

# Selects the game mode type
def GameModeSelector():
    pass

def Exit():
    print("Quitting...")
    time.sleep(1.5)
    sys.exit()

def IsValidOption(option, options):
    try:
        # Attempt to cast to an int
        option = int(option)

        if option not in options:
            return False
    except ValueError:
        return False
    except OverflowError:
        return False

    return True

def main():

    while True:
        # Display the user's options and get their response
        option = GettingStarted()

        if option == 1:
            print("Rules")
            Rules()
            continue
        elif option == 2:
            pass
        elif option == 3:
            Exit()

main()
