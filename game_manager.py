# GameManager Class
# Singleton
# This class manages the Connect Four game. It handles the game logic
# and handles interactions between the Board Class and Player Class

import time
import random
import pygame
import sys
from board import Board
from player import Player
from connect4_ui import Connect4UI

class GameManager:
    instance = None

    # Ensure that only one instance of this class exists
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.rows = 6
        self.cols = 7

        self.ui = Connect4UI(self.rows, self.cols)
        self.board = Board(self.rows, self.cols)

        self.player1 = Player("Player 1", 1, "X")
        self.player2 = Player("Opponent", 2, "O")

        self.current_player = self.player1

        self.game_mode = None
        self.is_game_over = False

    # Allows the player to customize their information. Takes in an integer 'game_mode'
    # as a parameter. The method uses the game_mode type to determine how to assign
    # the second player
    def SetPlayersInfo(self, game_mode):  # 1. Player vs Computer, 2. Player vs Player, 3. Computer vs Computer
        # Player chooses to be Player 1
        if self.ChoosePlayerNumber() == self.player1.GetPlayerNumber():
            self.player1.SetAsHuman()
            self.player1.SetPlayerName(self.ChoosePlayerName(self.player1.GetPlayerName()))
            self.player1.SetPlayerToken(self.ChoosePlayerToken())

            # Player vs Computer. Set Player 2 to Computer
            if game_mode == 1:
                self.player2.SetPlayerName("Opponent")
                if self.player1.GetPlayerToken() == "X":
                    self.player2.SetPlayerToken("O")
                else:
                    self.player2.SetPlayerToken("X")
        else:
            # Player chooses to be player 2
            self.player2.SetAsHuman()
            self.player2.SetPlayerName(self.ChoosePlayerName(self.player2.GetPlayerName()))
            self.player2.SetPlayerToken(self.ChoosePlayerToken())

            # Player vs Computer. Set player 1 to Computer
            if game_mode == 1:
                self.player1.SetPlayerName("Opponent")
                if self.player2.GetPlayerToken() == "X":
                    self.player1.SetPlayerToken("O")
                else:
                    self.player1.SetPlayerToken("X")

    # Allows the player to choose whether they take the first or second move
    def ChoosePlayerNumber(self):
        while True:
            print("Are you Player 1 or Player 2? (Player 1 has the first turn)")
            print("Pressing enter without a response will randomly assign a Player ID.")
            number = input(f"Enter 1 or 2:  ").strip()

            if number == "":
                number = random.randint(1, 2)
                break
            elif number not in ["1", "2"]:
                print("Invalid entry, please try again...")
                continue
            else:
                break

        print(f"You are Player {number}!\n")
        return int(number)

    # Allow the player to choose their token style (X or O)
    def ChoosePlayerToken(self):
        while True:
            print("Choose your token (X, O)")
            print("Pressing enter without a response will randomly assign a token: ")
            token = input("Enter X or O: ").strip().upper()

            if token == "":
                token = random.choice(["X", "O"])
                break
            if token not in ["X", "O"]:
                print("Invalid entry, please try again...")
                continue
            else:
                break

        print(f"Your token is {token}!\n")
        return token

    # Gets the player's name to personalize their experience
    def ChoosePlayerName(self, default_player_name):
        while True:
            char_limit = 10
            print(f"What would you like to be called?")
            print("Pressing enter without a response will assign your Player ID as your name: ")
            name = input(f"Choose your name ({char_limit} character limit): ")

            if name == "":
                print(f"You'll be called {default_player_name}\n")
                return default_player_name
            elif name.lower() == "computer":
                print(f"To prevent confusion, the name \"{name}\" is not available to Players.")
                continue
            elif len(name) > char_limit:
                print(f"Only the first {char_limit} characters of your name will be stored.")

                while True:
                    option = input(f"Is {name[:10]} okay? (yes, no): ").lower().strip()

                    if option in ["yes", "y"]:
                        print(f"Great! You'll be called {name[:10]}.\n")
                        return name
                    elif option in ["no", "n"]:
                        break
                    else:
                        print("Option invalid or unavailable...\n")
                        continue
            else:
                print(f"Great! You'll be called {name[:10]}.\n")
                return name[:10]

    # Defines the logic for the Main Menu
    def DisplayMainMenu(self):
        self.ui.InitWindow()
        self.ui.DrawMainMenuUI()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if a button was clicked
                    if self.ui.play_btn.collidepoint(mouse_pos):
                        self.PlayGame()
                        break
                    elif self.ui.rules_btn.collidepoint(mouse_pos):
                        self.DisplayRules()
                        break
                    elif self.ui.options_btn.collidepoint(mouse_pos):
                        self.DisplayOptions()
                        break
                    elif self.ui.exit_btn.collidepoint(mouse_pos):
                        sys.exit()

            pygame.display.update()

    def DisplayRules(self):
        file = 'v3_rules.txt'
        with open(file, 'r') as file:
            rules_text = file.read()
        file.close()

        self.ui.DrawRulesUI(rules_text)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.ui.back_btn.collidepoint(mouse_pos):
                        self.DisplayMainMenu()
                        break

    def DisplayOptions(self):
        self.ui.DrawOptionsUI()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.ui.player_btn.collidepoint(mouse_pos):
                        if self.ui.player_toggle == "Player 1":
                            self.ui.player_toggle = "Player 2"
                        else:
                            self.ui.player_toggle = "Player 1"
                    elif self.ui.color_btn.collidepoint(mouse_pos):
                        if self.ui.player_color == "Red":
                            self.ui.player_color = "Yellow"
                            self.ui.color_toggle = self.ui.color_yellow
                        else:
                            self.ui.player_color = "Red"
                            self.ui.color_toggle = self.ui.color_red
                    elif self.ui.back_btn.collidepoint(mouse_pos):
                        self.DisplayMainMenu()
                        break

                    # Handles checking in the input box is clicked
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.ui.name_input_box.collidepoint(pygame.mouse.get_pos()):
                            self.ui.input_active = True
                        else:
                            self.ui.input_active = False

                # Handle getting keystrokes for the users name
                elif self.ui.input_active and event.type == pygame.KEYDOWN:
                    # Handle backspace
                    if event.key == pygame.K_BACKSPACE:
                        self.ui.name_input_text = self.ui.name_input_text[:-1]
                    # Handle return/enter
                    elif event.key == pygame.K_RETURN:
                        pass
                    # Handle other characters
                    else:
                        self.ui.name_input_text += event.unicode

            self.ui.DrawOptionsUI()

    # Defines the logic for Player Vs Computer
    def PlayGame(self):
        self.board.ResetBoard()
        self.ui.InitWindow()
        self.ui.DrawBoardUI(self.board.GetGameBoard())

        self.player1.SetAsHuman()

        prev_hover_col = 1

        while not self.is_game_over:
            player_token = self.current_player.GetPlayerToken()

            # current_player is controlled by a person
            if self.current_player.isHuman:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    #  Track the player's mouse to display the column they are hovering over
                    if event.type == pygame.MOUSEMOTION:
                        # Draw the player's token in the current column they are hovering
                        hovering_col = self.ui.ConvertMousePos((event.pos[0])) + 1
                        self.board.TempUpdateBoard(hovering_col, player_token)
                        self.ui.DrawBoardUI(self.board.GetGameBoard())

                        # Remove player token from the previous column
                        if hovering_col != prev_hover_col:
                            self.board.UndoTemporaryBoardUpdate(prev_hover_col)
                            prev_hover_col = hovering_col

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Pass the first (x/horizontal) value of the tuple. The x value aligns with the col number
                        player_choice = self.ui.ConvertMousePos(event.pos[0]) + 1
                        self.board.UpdateBoard(player_choice, player_token)
                        self.ui.DrawBoardUI(self.board.GetGameBoard())

                        # Check if player's move resulted in 4 in a row
                        if self.board.CheckFourInARow(player_token, player_choice):
                            self.is_game_over = self.PlayAgain(self.current_player.GetPlayerName())
                            continue

                        # Change the current player
                        self.SwapTurn()

            # current_player is controlled by the computer
            else:
                time.sleep(0.5)
                player_choice = self.RandomMove()
                self.board.UpdateBoard(player_choice, player_token)
                self.ui.DrawBoardUI(self.board.GetGameBoard())

                # Check if computer's move resulted in 4 in a row
                if self.board.CheckFourInARow(player_token, player_choice):
                    self.is_game_over = self.PlayAgain(self.current_player.GetPlayerName())
                    continue

                # Change the current player
                self.SwapTurn()

            self.ui.DrawBoardUI(self.board.GetGameBoard())

            # End the game if the board is full
            if self.board.IsBoardFull():
                self.is_game_over = self.PlayAgain(None)

        pygame.quit()

    # Allows the player to decide if they would like to play again or quit
    def PlayAgain(self, winner):
        self.ui.DrawPlayAgainUI(winner)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if a button was clicked
                    if self.ui.play_again_btn.collidepoint(mouse_pos):
                        self.PlayGame()
                        return True
                    elif self.ui.menu_btn.collidepoint(mouse_pos):
                        self.DisplayMainMenu()

            pygame.display.update()

    # Generates a random move
    def RandomMove(self):
        num_rows, num_cols = self.board.GetBoardSize()
        tokens_per_col = self.board.GetTokensPerColumn()

        while True:
            random_move = int(random.randint(1, num_cols))
            if tokens_per_col[random_move] < num_rows:
                break

        return random_move

    # Change the current player
    def SwapTurn(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
