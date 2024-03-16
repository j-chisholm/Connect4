# GameManager Class
# This class manages the Connect Four game. It handles the game logic
# and handles interactions between the Board Class and Player Class

import time

from board import Board
from player import Player

class GameManager:

    def __init__(self):
        self.game_board = Board()
        self.player1 = None
        self.player2 = None

    def PlayGame(self):
        pass

    def PlayAgain(self):
        yes = ['y', 'yes']
        no = ['n', 'no']

        # Gives the player 3 attempts to enter a valid input
        for i in range(2, -1, -1):
            user_input = input("Would you like to play again? [yes, no]: ").lower()
            if user_input in yes:
                print("Resetting the game...")
                self.game_board = Board()  # Restart the game
                time.sleep(2)
                self.game_board.DisplayBoard()
                return False
            elif user_input in no:
                print("Exiting...")
                return True
            elif i > 0:
                print(f"Not a valid input. The game will exit after {i} more invalid inputs...\n")

        print("No more attempts remaining, game will now end...")
        return True

    # Prompts the player for an input and stores it
    def GetPlayerChoice(self, current_player):
        # Print instructions to the player
        print(f"\nPlayer {current_player}'s turn...")
        current_player = input("Enter a column (1-7) to to drop your token: ")


    def IsChoiceValid(self, player_choice):
        if player_choice == '':
            print("\nNo value entered.\nPlease try again!")
            return False
        try:
            player_choice = int(player_choice)
            if player_choice not in range(1, self.game_board.num_cols + 1):
                print("\nSorry, that choice is not in the range 1-7.\nPlease try again!")
            # check if the column is full
            elif self.game_board.num_tokens_per_col[player_choice] >= self.game_board.num_rows:
                print("\nThat column is full, please try again!")
                return False
            else:
                return True
        except ValueError:
            print("\nThat is not a number, please try again!")
            return False
        except OverflowError:
            print("That number is too large, please try again!")