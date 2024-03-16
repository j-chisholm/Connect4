import sys
import time
from game_manager import GameManager

# Provides the user a list of options at the beginning of the game
def GettingStarted():
    while True:
        print("Welcome to Connect 4.")
        print("1. Read the rules")
        print("2. Play Game")
        print("3. Quit")

        option = input("What would you like to do? ")

        print()  # Empty line for clarity

        if IsValidOption(option, [1, 2, 3]):
            option = int(option)
            break

        print("Option invalid or unavailable...\n")

    return option

# Reads the rules from an external file and presents it to the player
def Rules():
    file = 'rules.txt'
    with open(file, 'r') as file:
        for line in file:
            print(line, end='')
    file.close()

# Selects the game mode type
def GameModeSelector():
    while True:
        print("Choose your game mode.")
        print("1. Play against the Computer")
        print("2. coming soon...")

        option = input("What would you like to do? ")

        print()  # Empty line for clarity

        if IsValidOption(option, [1]):
            option = int(option)
            break

        print("Option invalid or unavailable...\n")

    return option

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

    gm = GameManager()

    while True:
        # Display the user's options and get their response
        option = GettingStarted()  # 1. Rules, 2. GameMode, 3. Quit

        if option == 1:
            Rules()
            continue # Return to the top of the while loop to display options again
        elif option == 2:
            mode = GameModeSelector() # 1. Vs Computer

            if mode == 1:
                gm.PlayPVC()

        elif option == 3:
            Exit()

main()
