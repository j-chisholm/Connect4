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

        self.player1 = Player("Player", 1, "X")
        self.player2 = Player("Computer", 2, "O")
        self.player = self.player1
        self.computer = self.player2

        self.current_player = self.player1

        self.is_game_over = False
        self.is_random_first_turn = True
        self.player_has_first_turn = True

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
                    # Toggle player token color
                    if self.ui.token_btn.collidepoint(mouse_pos):
                        if self.ui.token_btn_label == "Token: Red":
                            self.computer.SetPlayerToken("X")
                            self.player.SetPlayerToken("O")

                            self.ui.token_btn_label = "Token: Yellow"
                            self.ui.token_btn_color = self.ui.color_yellow
                        else:
                            self.computer.SetPlayerToken("O")
                            self.player.SetPlayerToken("X")

                            self.ui.token_btn_label = "Token: Red"
                            self.ui.token_btn_color = self.ui.color_red
                    # Toggle first turn
                    elif self.ui.first_move_btn.collidepoint(mouse_pos):
                        if self.ui.first_move_label == "Player has first turn":
                            self.ui.first_move_label = "Computer has first turn"
                            self.player_has_first_turn = False
                        elif self.ui.first_move_label == "Computer has first turn":
                            self.ui.first_move_label = "Random first turn"
                            self.is_random_first_turn = True
                        else:
                            self.ui.first_move_label = "Player has first turn"
                            self.player_has_first_turn = True
                            self.is_random_first_turn = False
                    # Handles the back button
                    elif self.ui.back_btn.collidepoint(mouse_pos):
                        self.DisplayMainMenu()
                        break
                    ''' * * * NAME INPUT FUNCTIONALITY REMOVED * * *
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
                        self.ui.name_input_text += event.unicode '''

            self.ui.DrawOptionsUI()

    # Defines the logic for Player Vs Computer
    def PlayGame(self):
        self.board.ResetBoard()
        self.ui.InitWindow()
        self.ui.DrawBoardUI(self.board.GetGameBoard())

        self.player.SetAsHuman()
        self.computer.SetAsComputer()

        prev_hover_col = 1

        if self.is_random_first_turn:
            self.RandomizeFirstTurn()

        if self.player_has_first_turn:
            self.current_player = self.player
        else:
            self.current_player = self.computer

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

    # Randomizes who has the first turn in the next game
    def RandomizeFirstTurn(self):
        if random.randint(1, 2) == 1:
            self.player_has_first_turn = True
        else:
            self.player_has_first_turn = False
