# UI Class
# This class handles displaying the interface which the user will use to interact with the Connect 4 game

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

    # Initialize board UI
    def InitBoard(self):
        # Determine the size of the window by the size of the board
        self.cell_size = 100
        self.win_width = self.cols * self.cell_size
        self.win_height = self.rows * self.cell_size

    # Draws the board UI on the game window
    def DrawBoardUI(self):
        # Draw the blue background
        self.window.fill(self.color_blue)

        # Draw the circles
        for row in range(self.rows + 1):
            for col in range(self.cols):
                cell_height = row * self.cell_size
                cell_width = col * self.cell_size

                circ_radius = (self.cell_size / 2) - 5  # Radius is half width of the rectangle, 5 is arbitrary
                circ_center = (int(cell_height + self.cell_size / 2), int(cell_width + self.cell_size/2))
                pygame.draw.circle(self.window, self.color_zero_alpha, circ_center, circ_radius)

        pygame.display.update()  # Pygame requires this function call after any display changes

ui = Connect4UI(6, 7)
ui.InitBoard()
ui.InitWindow()
ui.DrawBoardUI()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
