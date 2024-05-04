# Board Class
# Singleton
# This class represents the game board for Connect Four. It handles
# the board state including updating the board and checking for
# winning conditions.

class Board:
    instance = None

    # Ensure that only one instance of this class exists
    def __new__(cls, rows, cols):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    # __init__ method called at object instantiation
    def __init__(self, rows, cols):
        # Set the board size
        self.num_rows = rows
        self.num_cols = cols

        # Default values for the board labels
        self.row_labels = None
        self.col_labels = None

        # Default container types for tracking board state
        self.game_board = []
        self.num_tokens_per_col = {}

    # Resets the board to its default state
    def ResetBoard(self):
        # Set the labels for the rows and columns
        self.row_labels = ['f', 'e', 'd', 'c', 'b', 'a']
        self.col_labels = [str(i) for i in range(1, self.num_cols + 1)]

        # Default the number of tokens per column to 0
        self.num_tokens_per_col = {col: 0 for col in range(1, self.num_cols + 1)}

        # Default each space in the game board to an empty space
        self.game_board = []
        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                row.append(' ')
            self.game_board.append(row)

    # Updates the game board with a player's token in the given column
    # Updates the number of tokens in each column
    def UpdateBoard(self, player_choice, player_token):
        # Board[0][0] is at the top left of the game board, so the value
        # in 'row' is inverted
        row = self.num_tokens_per_col[player_choice]

        # To fix 'row', subtract from 1 then subtract from the total rows on the board
        # Subtract 1 from player_choice to because its value is 1-7 and, but lists are 0-indexed
        self.game_board[self.num_rows - 1 - row][player_choice - 1] = player_token

        # Update the number of tokens in the column by 1
        self.num_tokens_per_col[player_choice] = self.num_tokens_per_col[player_choice] + 1

    # Temporarily updates the game board as the player hovers over the columns
    def TempUpdateBoard(self, hovering_col, player_token):
        # Update the game board but *do not* update the number of entries in the column
        row = self.num_tokens_per_col[hovering_col]
        if row < self.num_rows:
            self.game_board[self.num_rows - 1 - row][hovering_col - 1] = player_token

    # Reset the board to the previous board state
    def UndoTempBoardUpdate(self, hovering_col):
        row = self.num_tokens_per_col[hovering_col]

        # If statement prevents the tokens at the bottom of the row from being removed
        if row < self.num_rows:
            self.game_board[self.num_rows - 1 - row][hovering_col - 1] = ' '

    # Checks if there are no more empty spaces on the board. Returns a boolean value
    def IsBoardFull(self):
        for num_tokens in self.num_tokens_per_col.values():
            if num_tokens != self.num_rows:
                return False
        return True

    # Checks the board to determine if there are 4 of the same tokens in a row. Returns a boolean value
    def CheckFourInARow(self, player_token, player_choice):
        start_row = self.num_rows - self.num_tokens_per_col[player_choice]
        start_col = player_choice - 1

        # Check for four in a row horizontally
        if (self.NumAdjacentTokens(player_token, start_row, start_col, 0, 1) +
                self.NumAdjacentTokens(player_token, start_row, start_col, 0, -1)) >= 3:
            return True

        # Check for four in a row vertically
        if (self.NumAdjacentTokens(player_token, start_row, start_col, 1, 0) +
                self.NumAdjacentTokens(player_token, start_row, start_col, -1, 0)) >= 3:
            return True

        # Check for four in a row on positive (up-right) diagonals
        if (self.NumAdjacentTokens(player_token, start_row, start_col, 1, 1) +
                self.NumAdjacentTokens(player_token, start_row, start_col, -1, -1)) >= 3:
            return True

        # Check for in a row on negative (down-right) diagonals
        if (self.NumAdjacentTokens(player_token, start_row, start_col, -1, 1) +
                self.NumAdjacentTokens(player_token, start_row, start_col, 1, -1)) >= 3:
            return True

        # If execution reaches this line, 4 in a row was not found
        return False

    # Checks for adjacent tokens in a single direction.
    # Returns the number of tokens found. Parameters row_increment, col_increment can be passed -1, 0, 1
    # to dictate which direction the function checks for adjacent matching tokens
    def NumAdjacentTokens(self, player_token, row_index, col_index, row_increment, col_increment):
        count = 0

        # Try block catches the instance where the function searches out of bounds for a player token
        try:
            # Only checks the next 3 spaces in a given direction.
            # No need to check that the player's current move matches their token
            for i in range(3):
                # Move to the next adjacent space
                row_index += row_increment
                col_index += col_increment

                # Due to a feature of lists, Python does not throw an index error for indexes that are negative.
                # Instead, it "wraps" around to the other end of the list.
                # Custom bounds checking and raise an IndexError if either index is negative.
                if row_index < 0 or col_index < 0:
                    raise IndexError

                # If a consecutive, similar token was found, increase count, otherwise return count
                if self.game_board[row_index][col_index] == player_token:
                    count += 1
                else:
                    break
            return count

        # Function reached the end of the board before 3 matching tokens were found
        except IndexError:
            return count

    # Returns the tokens per column tracker (dictionary)
    def GetTokensPerColumn(self):
        return self.num_tokens_per_col

    # Returns the board size as a list [num_rows, num_col]
    def GetBoardSize(self):
        return self.num_rows, self.num_cols

    # Returns the game board
    def GetGameBoard(self):
        return self.game_board
