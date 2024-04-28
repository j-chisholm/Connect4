# UI Class
# This class handles displaying the interface which the user will use to interact with the Connect 4 game
import math

import pygame
import sys


class Connect4UI:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.cell_size = 100

        self.window = None
        self.win_width = self.cols * self.cell_size
        self.win_height = self.rows * self.cell_size

        self.color_yellow = (255, 223, 0)
        self.color_red = (255, 69, 58)
        self.color_blue = (0, 104, 255)
        self.color_black = (0, 0, 0)
        self.color_white = (255, 255, 255)
        self.color_zero_alpha = (0, 0, 0, 0)

        self.play_btn = None
        self.rules_btn = None
        self.options_btn = None
        self.exit_btn = None
        self.menu_btn = None
        self.back_btn = None
        self.play_again_btn = None
        self.player_btn = None
        self.color_btn = None

        self.name_input_box = None
        self.name_input_text = ""
        self.input_active = False
        self.show_cursor = True
        self.last_cursor_toggle = pygame.time.get_ticks()

        pygame.init()  # Initialize pygame

    # Initializes the game window
    def InitWindow(self):
        window_size = (self.win_width, self.win_height)
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Connect 4")

    # Draws the button to the window
    def DrawButton(self, font, text, x, y, width, height, btn_color=(0, 0, 0)):
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.window, btn_color, button_rect)
        pygame.draw.rect(self.window, self.color_white, button_rect, width=2)
        text_surface = font.render(text, True, self.color_white)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.window.blit(text_surface, text_rect)

        # Return the button rect after drawing, so it can be used to determine if it was clicked
        return button_rect

    # Displays the Main Menu
    def DrawMainMenuUI(self):
        # Define font
        font = pygame.font.Font(None, 40)

        # General button properties
        btn_width = 200
        btn_height = 50
        btn_x = (self.win_width - btn_width) // 2

        # Button vertical position
        space_btwn_btns = 50
        play_btn_y = (self.win_height // 2) - (2 * (btn_height + space_btwn_btns))
        rules_btn_y = (self.win_height // 2) - (btn_height + space_btwn_btns)
        options_btn_y = (self.win_height // 2)
        exit_btn_y = (self.win_height // 2) + (btn_height + space_btwn_btns)

        # Fill the window with blue
        self.window.fill(self.color_blue)

        # Draw the buttons and get their rects
        self.play_btn = self.DrawButton(font, "Play", btn_x, play_btn_y, btn_width, btn_height)
        self.rules_btn = self.DrawButton(font, "Rules", btn_x, rules_btn_y, btn_width, btn_height)
        self.options_btn = self.DrawButton(font, "Options", btn_x, options_btn_y, btn_width, btn_height)
        self.exit_btn = self.DrawButton(font, "Exit", btn_x, exit_btn_y, btn_width, btn_height)

        pygame.display.update()

    # Displays the rules
    def DrawRulesUI(self, text):
        # Define font
        rules_font = pygame.font.Font(None, 24)
        btn_font = pygame.font.Font(None, 40)

        # Fill the background with blue
        self.window.fill(self.color_blue)

        # Split text by newlines for multiline rendering
        lines = text.split('\n')

        # Starting position for rendering text
        x = 50
        y = 50

        # Render each line of text
        for line in lines:
            txt_img = rules_font.render(line, True, self.color_white)
            self.window.blit(txt_img, (x, y))
            # Move the y position down to create space between each line
            y += rules_font.get_height() + 10

        # General button properties
        self.back_btn = self.DrawButton(btn_font, "Back", self.win_width // 2, 400, 200, 50)

        # Update the display to show the changes
        pygame.display.update()

    # Displays the options
    def DrawOptionsUI(self):
        # Define font
        font = pygame.font.Font(None, 40)

        # Define smaller font for input boxes, labels, and instructions
        small_font = pygame.font.Font(None, 30)
        instruction_font = pygame.font.Font(None, 24)

        # Button and input properties
        btn_width = 200
        btn_height = 50
        input_width = 300
        input_height = 40
        input_x = (self.win_width - input_width) // 2

        # Positions for elements
        space_btwn_elements = 30
        initial_y = self.win_height // 2 - 2 * (btn_height + space_btwn_elements)

        # Fill the window with the background color
        self.window.fill(self.color_blue)

        # Draw name label and input box
        name_label = small_font.render("Enter Your Name:", True, self.color_white)
        name_label_rect = name_label.get_rect(center=(self.win_width // 2, initial_y - 30))
        self.window.blit(name_label, name_label_rect)
        self.name_input_box = pygame.Rect(input_x, initial_y, input_width, input_height)
        pygame.draw.rect(self.window, self.color_white, self.name_input_box)

        # Draw the input text inside the input box
        input_text_surface = small_font.render(self.name_input_text, True, self.color_black)
        self.window.blit(input_text_surface, (input_x + 5, initial_y + 5))

        # Toggle caret on and off to identify cursor location in input box
        current_time = pygame.time.get_ticks()
        if current_time - self.last_cursor_toggle >= 500:
            self.show_cursor = not self.show_cursor
            self.last_cursor_toggle = current_time

        # Draw the cursor if active and visible
        if self.input_active and self.show_cursor:
            cursor_x = input_x + small_font.size(self.name_input_text)[0] + 5
            pygame.draw.line(self.window, self.color_black, (cursor_x, initial_y + 5),
                             (cursor_x, initial_y + input_height - 5), 2)

        # Adjust initial_y for the next elements
        initial_y += input_height + space_btwn_elements

        # Add instruction text above the player button
        instruction_text = instruction_font.render("Click to toggle between options", True, self.color_white)
        instruction_text_rect = instruction_text.get_rect(center=(self.win_width // 2, initial_y - 10))
        self.window.blit(instruction_text, instruction_text_rect)

        # Adjust initial_y for the instruction text
        initial_y += 15

        # Player choice button
        player_btn_y = initial_y
        player_btn_x = (self.win_width - btn_width) // 2
        self.player_btn = self.DrawButton(font, "Player 1", player_btn_x, player_btn_y, btn_width, btn_height)

        # Adjust initial_y for the next elements
        initial_y += btn_height + space_btwn_elements

        # Color choice button
        color_btn_y = initial_y
        color_btn_x = (self.win_width - btn_width) // 2
        self.color_btn = self.DrawButton(font, "Red", color_btn_x, color_btn_y, btn_width, btn_height, self.color_red)

        # Draw back button in the lower right corner
        back_btn_y = self.win_height - btn_height - 20  # 20 pixels padding from bottom
        back_btn_x = self.win_width - btn_width - 20  # 20 pixels padding from right
        self.back_btn = self.DrawButton(font, "Back", back_btn_x, back_btn_y, btn_width, btn_height)

        # Update the display
        pygame.display.update()

    # Draws the board UI on the game window
    def DrawBoardUI(self, board):
        # Fill the background with blue
        self.window.fill(self.color_blue)

        # Draw the background circles
        for row in range(self.rows):
            for col in range(self.cols):
                cell_height = col * self.cell_size
                cell_width = row * self.cell_size

                # Radius is half the width of the cell's size (square around the circle)
                # Subtract an arbitrary number which will represent the width of the boarder between cells
                circ_radius = (self.cell_size / 2) - 4
                circ_center = (int(cell_height + self.cell_size / 2), int(cell_width + self.cell_size / 2))

                if board[row][col] == "X":
                    pygame.draw.circle(self.window, self.color_red, circ_center, circ_radius)
                elif board[row][col] == "O":
                    pygame.draw.circle(self.window, self.color_yellow, circ_center, circ_radius)
                else:
                    pygame.draw.circle(self.window, self.color_zero_alpha, circ_center, circ_radius)

        pygame.display.update()  # Pygame requires this function call after any display changes

    def DrawPlayAgainUI(self, winner):
        # Define button font
        button_font = pygame.font.Font(None, 24)

        # Define font for "Game Over" text
        game_over_font = pygame.font.Font(None, 60)

        # General button properties
        btn_width = 200
        btn_height = 50
        btn_y = (self.win_height - btn_height) // 2

        # Button horizontal position
        space_btwn_btns = 50
        play_again_btn_x = (self.win_width // 2) - btn_width - space_btwn_btns
        menu_btn_x = (self.win_width // 2) + space_btwn_btns

        # Define vertical position for the "Game Over" text
        title_y = btn_y - (2 * btn_height)

        # Render "Game Over" text
        if winner is not None:
            end_game_text = f"{winner} wins!"
        else:
            end_game_text = "Draw!"

        game_over_text = game_over_font.render(end_game_text, True, self.color_white)
        game_over_rect = game_over_text.get_rect(center=(self.win_width // 2, title_y))

        # Draw "Game Over" text to the window
        self.window.blit(game_over_text, game_over_rect)

        # Draw the buttons and get their rects
        self.play_again_btn = self.DrawButton(button_font, "Play Again", play_again_btn_x, btn_y, btn_width,
                                              btn_height)
        self.menu_btn = self.DrawButton(button_font, "Main Menu", menu_btn_x, btn_y, btn_width, btn_height)

        # Update the display to show the changes
        pygame.display.update()

    # Converts the horizontal position of the mouse to a value between 0 and the total number of columns
    def ConvertMousePos(self, mouse_xpos):
        # Convert the horizontal value to an equivalent value between 0 and 6 by dividing by the cell size
        # Math.floor to round the number down and force it to an int at the same time
        return math.floor(mouse_xpos / self.cell_size)

    def DrawText(self, text, font, text_color, x_pos, y_pos):
        img = font.render(text, True, text_color)
        self.window.blit(img, (x_pos, y_pos))
