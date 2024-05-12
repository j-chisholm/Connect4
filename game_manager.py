# GameManager Class
# Singleton
# This class manages the Connect Four game. It handles the game logic
# and handles interactions between the Board Class and Player Class
import math
import random
import pygame
import sys
import copy
import threading
from ai_manager import AIManager
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

    # __init__ method called at object instantiation
    def __init__(self):
        self.rows = 6
        self.cols = 7

        # Instantiate UI and Board objects
        self.ui = Connect4UI(self.rows, self.cols)
        self.board = Board(self.rows, self.cols)

        # Initialize the AI
        self.ai = AIManager(self.rows, self.cols)
        self.depth = 0

        self.sleep_time = 250

        # Set default player values
        self.player1 = Player("Player", 1, "X")
        self.player2 = Player("Computer", 2, "O")
        self.player = self.player1
        self.computer = self.player2

        # Player 1 has first turn by default
        self.current_player = self.player1

        # Set default game loop variables
        self.is_game_over = False
        self.is_random_first_turn = True
        self.player_has_first_turn = True

        # Set default score tracking variables
        self.total_games = 0
        self.red_wins_1st_turn = 0  # How many times red wins if it had 1st turn
        self.red_wins_2nd_turn = 0  # How many times red wins if it had 2nd turn
        self.red_draws_2nd_turn = 0  # How many times red draws if it had 2nd turn
        self.yellow_wins_1st_turn = 0  # How many times yellow wins if it had 1st turn
        self.yellow_wins_2nd_turn = 0  # How many times yellow wins if it had 2nd turn
        self.yellow_draws_2nd_turn = 0  # How many times yellow draws if it had 2nd turn

    # Defines the logic for displaying and interacting with the main menu
    def DisplayMainMenu(self):
        # Initialize the menu and display the main
        self.ui.InitWindow()
        self.ui.DrawMainMenuUI()

        # Main Menu loop
        while True:
            for event in pygame.event.get():
                # If the 'x' button is clicked
                if event.type == pygame.QUIT:
                    sys.exit()
                # On mouse clicks...
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if a button was clicked
                    if self.ui.play_btn.collidepoint(mouse_pos):
                        self.PlayGame()  # Play the game
                        break
                    elif self.ui.rules_btn.collidepoint(mouse_pos):
                        self.DisplayRules()  # Display the rules
                        break
                    elif self.ui.options_btn.collidepoint(mouse_pos):
                        self.DisplayOptions()  # Show the options menu
                        break
                    elif self.ui.exit_btn.collidepoint(mouse_pos):
                        sys.exit()  # Exit the game

            pygame.display.update()

    # Defines the logic for displaying the rules
    def DisplayRules(self):
        # Set the local file path for the rules text file
        file = 'v3_rules.txt'

        # Open the file and store the rules text
        with open(file, 'r') as file:
            rules_text = file.read()
        file.close()

        # Display the rules on the UI
        self.ui.DrawRulesUI(rules_text)

        # Main Rules UI loop
        while True:
            for event in pygame.event.get():
                # Quit if the 'x' button is clicked
                if event.type == pygame.QUIT:
                    sys.exit()
                # On mouse clicks...
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    mouse_pos = pygame.mouse.get_pos()
                    if self.ui.back_btn.collidepoint(mouse_pos):
                        self.DisplayMainMenu()  # Return to the main menu
                        break

    # Defines the logic for displaying the options
    def DisplayOptions(self):
        # Display the options window
        self.ui.DrawOptionsUI()

        # Main options UI loop
        while True:
            for event in pygame.event.get():
                # Quit ff the 'x' button was clicked
                if event.type == pygame.QUIT:
                    sys.exit()
                # On mouse clicks...
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    mouse_pos = pygame.mouse.get_pos()

                    # Toggle the player token between red and yellow
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

                    # Toggle the option for who has the first turn (player, computer, random)
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

                    # Return to the main menu
                    elif self.ui.back_btn.collidepoint(mouse_pos):
                        self.DisplayMainMenu()
                        break

                    ''' * * * NAME INPUT FUNCTIONALITY REMOVED * * *
                    # Activates the text box if it's clicked
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.ui.name_input_box.collidepoint(pygame.mouse.get_pos()):
                            self.ui.input_active = True
                        else:
                            self.ui.input_active = False
                            
                # Save and display the name the user enters in the text box
                elif self.ui.input_active and event.type == pygame.KEYDOWN:
                    # Remove 1 character if the player presses backspace
                    if event.key == pygame.K_BACKSPACE:
                        self.ui.name_input_text = self.ui.name_input_text[:-1]
                    # Do nothing if the player enters Enter/Return
                    elif event.key == pygame.K_RETURN:
                        pass
                    # Append all other characters to the player's name
                    else:
                        self.ui.name_input_text += event.unicode '''

            self.ui.DrawOptionsUI()  # Update the window by redrawing the options UI

    # Defines the logic for the main game loop
    def PlayGame(self):
        # Initialize the board and the window
        self.board.ResetBoard()
        #self.board.SetTestBoard()
        self.ui.InitWindow()

        # self.ai.ClearTranspositionTable()

        # Draw the UI to display the board
        self.ui.DrawBoardUI(self.board.GetGameBoard())

        # Sets the player to human-controlled and the computer to computer-controlled
        self.player.SetAsHuman()  # Change to player.SetAsComputer() to pit the AI against itself
        self.computer.SetAsComputer()

        self.ai.SetTokens(self.computer.GetPlayerToken(), self.player.GetPlayerToken())

        # Set an arbitrary default value for the col being hovered over
        prev_hover_col = 1

        # Apply player's chosen options
        if self.is_random_first_turn:
            self.RandomizeFirstTurn()  # Set the turn order to random

        if self.player_has_first_turn:
            self.current_player = self.player  # Set the turn order to player always has first turn
        else:
            self.current_player = self.computer  # Set the turn order to computer always has first turn

        self.current_player = self.player

        # Define the main game loop
        while not self.is_game_over:
            # Get the token of the active player
            player_token = self.current_player.GetPlayerToken()

            # Get a mouse input from the player
            if self.current_player.isHuman:
                for event in pygame.event.get():
                    # Quit if the 'x' button is clicked
                    if event.type == pygame.QUIT:
                        sys.exit()

                    #  Track the player's mouse to display the column they are hovering over
                    if event.type == pygame.MOUSEMOTION:
                        # Draw the player's token in the current column they are hovering
                        hovering_col = self.ui.ConvertMousePos((event.pos[0])) + 1  # +1 to account for 0-indexing
                        self.board.TempUpdateBoard(hovering_col, player_token)
                        self.ui.DrawBoardUI(self.board.GetGameBoard())

                        # Remove player token from the previous column they hovered over
                        if hovering_col != prev_hover_col:
                            self.board.UndoTempBoardUpdate(prev_hover_col)
                            prev_hover_col = hovering_col
                            self.ui.DrawBoardUI(self.board.GetGameBoard())

                    # On mouse clicks...
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Pass the first (x/horizontal) value of the tuple which aligns with the col number
                        player_choice = self.ui.ConvertMousePos(event.pos[0]) + 1  # +1 to account for 0-indexing

                        if self.board.GetTokensPerColumn()[player_choice] < self.board.num_rows:
                            # Update the board
                            self.board.UpdateBoard(player_choice, player_token)
                            self.ui.DrawBoardUI(self.board.GetGameBoard())

                            self.SwapTurn()

                        # Check if player's move resulted in 4 in a row
                        if self.board.CheckFourInARow(player_token, player_choice):
                            #self.KeepScore(player_token)
                            self.is_game_over = self.PlayAgain(self.current_player.GetPlayerName())
                            continue
                        # End the game if the board is full
                        elif self.board.IsBoardFull():
                            #self.KeepScore(player_token, win=False)
                            self.is_game_over = self.PlayAgain(None)

            # Get an input from the AI
            else:
                pygame.time.wait(self.sleep_time)  # Pieces appear suddenly, so wait a certain amount of time

                # Pick the optimal move
                ai_choice = self.AIMoveThread()

                # Update the board
                self.board.UpdateBoard(ai_choice, player_token)
                row = self.board.num_tokens_per_col[ai_choice]

                self.ui.DrawBoardUI(self.board.GetGameBoard())
                #print(self.board.GetTokensPerColumn())

                self.ai.first_time = True

                # Check if computer's move resulted in 4 in a row
                if self.board.CheckFourInARow(player_token, ai_choice):
                    #self.KeepScore(player_token)
                    self.is_game_over = self.PlayAgain(self.current_player.GetPlayerName())
                    continue
                # End the game if the board is full
                elif self.board.IsBoardFull():
                    # self.KeepScore(player_token, win=False)
                    self.is_game_over = self.PlayAgain(None)

                self.SwapTurn()  # Change the current player

            self.ui.DrawBoardUI(self.board.GetGameBoard())  # Update the window by redrawing the board

            pygame.time.wait(self.sleep_time)
        # pygame.quit()  # Quit the application after exiting the main game loop

    # Defines logic for restarting the game after a match has ended
    def PlayAgain(self, winner):
        self.ui.DrawBoardUI(self.board.GetGameBoard())  # Update the window by redrawing the board
        self.ui.DrawPlayAgainUI(winner)  # Draw the UI that prompts the user to play against

        # Defines the logic for the play again window
        while True:
            for event in pygame.event.get():
                # Quit if the 'x' button is clicked
                if event.type == pygame.QUIT:
                    sys.exit()
                # On mouse clicks...
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the mouse position
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if a button was clicked
                    if self.ui.play_again_btn.collidepoint(mouse_pos):
                        self.PlayGame()  # Play the game again
                        return True
                    elif self.ui.menu_btn.collidepoint(mouse_pos):
                        self.DisplayMainMenu()  # Return to the main menu

            pygame.display.update()  # Update the window with any visual changes

    # Swaps the active player
    def SwapTurn(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    # Randomizes who has the first turn in the *next* game
    def RandomizeFirstTurn(self):
        if random.randint(1, 2) == 1:
            self.player_has_first_turn = True
        else:
            self.player_has_first_turn = False

    def KeepScore(self, winning_token, win=True):
        self.total_games += 1

        # Game ended in a win
        if win:
            # If red won
            if winning_token == 'X':
                if self.player_has_first_turn:
                    self.red_wins_1st_turn += 1  # red won and had 1st turn
                else:
                    self.red_wins_2nd_turn += 1  # red won and had 2nd turn
            # If yellow won
            else:
                if self.player_has_first_turn:
                    self.yellow_wins_2nd_turn += 1  # yellow won and had 2nd turn
                else:
                    self.yellow_wins_1st_turn += 1  # yellow won and had 1st turn
        # Game ended in a draw
        else:
            if self.player_has_first_turn:
                self.yellow_draws_2nd_turn += 1  # yellow drawed from 2nd turn
            else:
                self.red_draws_2nd_turn += 1  # red drawed from 1st turn

        print(f"{self.total_games} games\n"
              f"Red won {self.red_wins_1st_turn} games as the 1st player\n"
              f"Red won {self.red_wins_2nd_turn} games as the 2nd player\n"
              f"Red drawed {self.red_draws_2nd_turn} games as the 2nd player\n"
              f"Yellow won {self.yellow_wins_1st_turn} games as the 1st player\n"
              f"Yellow won {self.yellow_wins_2nd_turn} games as the 2nd player\n"
              f"Yellow drawed {self.yellow_draws_2nd_turn} games as the 2nd player\n")

    def AIMoveThread(self):
        ai_choice = threading.Event()
        thread = threading.Thread(target=self.GetAIMove, args=(ai_choice,))
        thread.start()
        thread.join()

        return ai_choice.result

    def GetAIMove(self, ai_choice):
        self.CalculateSearchDepth()

        # Create a lock to synchronize access to ai_choice
        ai_choice_lock = threading.Lock()

        with ai_choice_lock:
            ai_choice.result = self.ai.MiniMax(copy.deepcopy(self.board), self.depth, -math.inf, math.inf,
                                               True)[1]

    def CalculateSearchDepth(self):
        if self.ai.DetermineBoardComplexity(self.board) <= 2:
            self.depth = 5
        elif self.ai.DetermineBoardComplexity(self.board) <= 6:
            self.depth = 6
        elif self.ai.DetermineBoardComplexity(self.board) <= 8:
            self.depth = 7
        elif self.ai.DetermineBoardComplexity(self.board) <= 10:
            self.depth = 8
        elif self.ai.DetermineBoardComplexity(self.board) <= 12:
            self.depth = 9
        else:
            self.depth = 10
