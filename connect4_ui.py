# UI Class
# This class handles displaying the interface which the user will use to interact with the Connect 4 game
import math

import pygame
import sys

class Connect4UI:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.cell_size = 0

        self.window = None
        self.win_width = None
        self.win_height = None

        self.color_yellow = (155, 155, 0)
        self.color_red = (255, 0, 0)
        self.color_blue = (0, 0, 255)
        self.color_black = (0, 0, 0)
        self.color_white = (255, 255, 255)
        self.color_zero_alpha = (0, 0, 0, 0)

        self.play_btn = None
        self.rules_btn = None
        self.options_btn = None
        self.exit_btn = None
        self.menu_btn = None

        pygame.init()  # Initialize pygame

    # Initializes the game window
    def InitWindow(self):
        window_size = (self.win_width, self.win_height)
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Connect 4")

    # Initialize board UI
    def InitBoard(self):
        # Determine the size of the window by the size of the board
        self.cell_size = 100
        self.win_width = self.cols * self.cell_size
        self.win_height = self.rows * self.cell_size

    # Draws the button to the window
    def DrawButton(self, font, text, x, y, width, height):
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.window, self.color_black, button_rect)
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
        btn_x = (self.win_width - btn_width)//2

        # Button vertical position
        space_btwn_btns = 50
        play_btn_y = (self.win_height//2) - (2 * (btn_height + space_btwn_btns))
        rules_btn_y = (self.win_height//2) - (btn_height + space_btwn_btns)
        options_btn_y = (self.win_height//2)
        exit_btn_y = (self.win_height//2) + (btn_height + space_btwn_btns)

        # Fill the window with blue
        self.window.fill(self.color_blue)

        # Draw the buttons and get their rects
        self.play_btn = self.DrawButton(font, "Play", btn_x, play_btn_y, btn_width, btn_height)
        self.rules_btn = self.DrawButton(font, "Rules", btn_x, rules_btn_y, btn_width, btn_height)
        self.options_btn = self.DrawButton(font, "Options", btn_x, options_btn_y, btn_width, btn_height)
        self.exit_btn = self.DrawButton(font, "Exit", btn_x, exit_btn_y, btn_width, btn_height)

        pygame.display.update()

    def DrawRulesUI(self, text):
        # Define font
        font = pygame.font.Font(None, 24)

        # Fill the background with blue
        self.window.fill(self.color_blue)

        # Split text by newlines for multiline rendering
        lines = text.split('\n')

        # Starting position for rendering text
        x = 50
        y = 50

        # Render each line of text
        for line in lines:
            txt_img = font.render(line, True, self.color_white)
            self.window.blit(txt_img, (x, y))
            # Move the y position down to create space between each line
            y += font.get_height() + 10

        # General button properties
        self.menu_btn = self.DrawButton(font, "Main Menu", self.win_width//2, 400, 200, 50)

        # Update the display to show the changes
        pygame.display.update()

    def DrawOptionsUI(self):
        pass

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
                circ_center = (int(cell_height + self.cell_size/2), int(cell_width + self.cell_size/2))

                if board[row][col] == "X":
                    pygame.draw.circle(self.window, self.color_red, circ_center, circ_radius)
                elif board[row][col] == "O":
                    pygame.draw.circle(self.window, self.color_yellow, circ_center, circ_radius)
                else:
                    pygame.draw.circle(self.window, self.color_zero_alpha, circ_center, circ_radius)

        pygame.display.update()  # Pygame requires this function call after any display changes

    # Converts the horizontal position of the mouse to a value between 0 and the total number of columns
    def ConvertMousePos(self, mouse_xpos):
        # Convert the horizontal value to an equivalent value between 0 and 6 by dividing by the cell size
        # Math.floor to round the number down and force it to an int at the same time
        return math.floor(mouse_xpos/self.cell_size)

    def DrawText(self, text, font, text_color, x_pos, y_pos):
        img = font.render(text, True, text_color)
        self.window.blit(img, (x_pos, y_pos))
