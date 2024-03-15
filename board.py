# Board Class
# This class represents the game board for Connect Four. It handles
# the board state including updating and displaying the board and
# checking for winning conditions.

class Board:

    def __init__(self):
        pass

    def InitializeGameBoard(self, rows, cols):
        pass

    def UpdateGameBoard(self, col, player_token):
        pass

    def DisplayGameBoard(self):
        pass

    def IsBoardFull(self):
        pass

    def CheckFourInARow(self, player_token, player_choice):
        pass

    def NumAdjacentTokens(self, player_token, start_row, start_col, row_increment, col_increment):
        pass
