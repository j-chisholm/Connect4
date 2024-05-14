# Main game script
# This file is the entry point into the game

from game_manager import GameManager

def main():
    # Create a game_manager game object
    gm = GameManager()

    # Display the main menu as entry to the game
    gm.PlayGame()

main()
