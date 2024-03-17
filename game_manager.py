# GameManager Class
# Singleton
# This class manages the Connect Four game. It handles the game logic
# and handles interactions between the Board Class and Player Class

import time
import random
from board import Board
from player import Player

class GameManager:

    instance = None

    # Ensure that only one instance of this class exists
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.board = Board(6, 7)

        self.player1 = Player(None, 1, None)
        self.player2 = Player(None, 2, None)

        self.current_player = self.player1

        self.game_mode = None
        self.is_game_over = False

    # Allows the player to customize their information
    def SetPlayersInfo(self):
        if self.ChoosePlayerNumber() == self.player1.GetPlayerNumber():
            print("Great! You'll be Player 1!")
            self.player1.SetPlayerName(self.ChoosePlayerName())
            # self.player1.SetPlayerToken(self.ChoosePlayerToken())
        else:
            print("Great! You'll be Player 2!")
            self.player2.SetPlayerName(self.ChoosePlayerName())
            # self.player2.SetPlayerToken(self.ChoosePlayerToken())

    # Allows the player to choose whether they take the first or second move
    def ChoosePlayerNumber(self):
        while True:
            print("Are you Player 1 or Player 2? (Player 1 has the first turn)")
            number = input(f"Enter 1 or 2:  ").strip()

            if number not in ["1", "2"] or number == "":
                print("Invalid entry, please try again...")
                continue
            else:
                return int(number)

    # Gets the player's name to personalize their experience
    def ChoosePlayerName(self):
        while True:
            char_limit = 10
            name = input(f"What would you like to be called? ({char_limit} character limit): ")

            if len(name) > char_limit:
                print(f"Only the first {char_limit} characters of your name will be stored.")

                while True:
                    option = input(f"Is {name[:10]} okay? (yes, no): ").lower().strip()

                    if option in ["yes", "y"]:
                        print(f"Great! You'll be called {name[:10]}.")
                        return name
                    elif option in ["no", "n"]:
                        break
                    else:
                        print("Option invalid or unavailable...\n")
                        continue
            else:
                break

        print(f"Great! You'll be called {name[:10]}.")
        return name[:10]

    # Allow the player to choose their token style (X or O)
    def ChoosePlayerToken(self):
        pass

    # Defines the logic for Player Vs Computer
    def PlayPVC(self):
        self.board.ResetBoard()
        self.board.DisplayBoard()

        self.player1.SetCurrentPlayer()
        self.player1.SetPlayerToken("X")
        self.player2.SetPlayerToken("0")

        while not self.is_game_over:
            # Determine whose turn it is
            if self.player1.IsCurrentPlayer():
                player_number = self.player1.GetPlayerNumber()
                player_token = self.player1.GetPlayerToken()

                # Continue to prompt user until they provide a valid move
                while True:
                    player_choice = self.GetPlayerChoice(self.current_player)

                    if not self.IsChoiceValid(player_choice):
                        # Pause execution to allow player time to read on screen instructions
                        time.sleep(1.5)
                        self.board.DisplayBoard()

                    # Player's move is valid and can be converted to INT
                    else:
                        player_choice = int(player_choice)
                        break

                self.board.UpdateBoard(player_choice, player_token)

                # Check if player's move resulted in 4 in a row
                if self.board.CheckFourInARow(player_token, player_choice):
                    self.board.DisplayBoard()
                    print(f"\nPlayer {player_number} wins!")
                    self.is_game_over = self.PlayAgain()
                    continue

                # Change the current player
                self.SwapTurn()
            else:
                print("\nComputer's turn...")
                time.sleep(1)

                player_token = self.player2.GetPlayerToken()

                player_choice = self.RandomMove()

                self.board.UpdateBoard(player_choice, player_token)

                # Check if player's move resulted in 4 in a row
                if self.board.CheckFourInARow(player_token, player_choice):
                    self.board.DisplayBoard()
                    print(f"\nComputer wins!")
                    self.is_game_over = self.PlayAgain()
                    continue

                # Change the current player
                self.SwapTurn()

            self.board.DisplayBoard()

            # End the game if the board is full
            if self.board.IsBoardFull():
                print('DRAW!')

    def PlayAgain(self):
        yes = ['y', 'yes']
        no = ['n', 'no']

        # Gives the player 3 attempts to enter a valid input
        for i in range(2, -1, -1):
            user_input = input("Would you like to play again? [yes, no]: ").lower()
            if user_input in yes:
                print("Resetting the game...")
                self.board.ResetBoard()  # Reset the game board
                time.sleep(2)
                self.board.DisplayBoard()
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
        print(f"\n{current_player.GetPlayerName()}'s turn...")
        player_choice = input("Enter a column (1-7) to to drop your token: ")

        return player_choice

    # Validate the user's input against the current board state
    def IsChoiceValid(self, player_choice):
        num_rows, num_cols = self.board.GetBoardSize()
        tokens_per_col = self.board.GetTokensPerColumn()

        if player_choice == '':
            print("\nNo value entered.\nPlease try again!")
            return False
        try:
            player_choice = int(player_choice)
            if player_choice not in range(1, num_cols + 1):
                print("\nSorry, that choice is not in the range 1-7.\nPlease try again!")
            # check if the column is full
            elif tokens_per_col[player_choice] >= num_rows:
                print("\nThat column is full, please try again!")
                return False
            else:
                return True
        except ValueError:
            print("\nThat is not a number, please try again!")
            return False
        except OverflowError:
            print("That number is too large, please try again!")

    # Generates a random move
    def RandomMove(self):
        num_rows, num_cols = self.board.GetBoardSize()
        tokens_per_col = self.board.GetTokensPerColumn()

        while True:
            random_move = int(random.randint(1, num_cols))
            if tokens_per_col[random_move] < num_rows:
                break

        return random_move

    # Swaps the player's turn to true or false
    def SwapTurn(self):
        if self.player1.IsCurrentPlayer():
            self.player1.SetNotCurrentPlayer()
            self.player2.SetCurrentPlayer()
        else:
            self.player2.SetNotCurrentPlayer()
            self.player1.SetCurrentPlayer()
