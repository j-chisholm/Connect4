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
        self.color_zero_alpha = (0, 0, 0, 0)

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

    # Draws the board UI on the game window
    def DrawBoardUI(self):
        # Fill the background with blue
        self.window.fill(self.color_blue)

        # Draw the circles
        for row in range(self.rows + 1):
            for col in range(self.cols):
                cell_height = row * self.cell_size
                cell_width = col * self.cell_size

                # Radius is half the width of the cell's size (square around the circle)
                # Subtract an arbitrary number which will represent the width of the boarder between cells
                circ_radius = (self.cell_size / 2) - 4
                circ_center = (int(cell_height + self.cell_size/2), int(cell_width + self.cell_size/2))
                pygame.draw.circle(self.window, self.color_zero_alpha, circ_center, circ_radius)

        pygame.display.update()  # Pygame requires this function call after any display changes

    # Converts the horizontal position of the mouse to a value between 0 and the total number of columns
    def ConvertMousePos(self, mouse_xpos):
        # Convert the horizontal value to an equivalent value between 0 and 6 by dividing by the cell size
        # Math.floor to round the number down and force it to an int at the same time
        return math.floor(mouse_xpos/ui.cell_size)

    # Handles populating the game board with the appropriately colored token
    def DropToken(self, mouse_position, color):
        pass


ui = Connect4UI(6, 7)
ui.InitBoard()
ui.InitWindow()
ui.DrawBoardUI()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Pass the first (x/horizontal) value of the tuple. The x value aligns with the col number
            player_choice = ui.ConvertMousePos(event.pos[0])
