# Board Class
# This class represents the game board for Connect Four. It handles
# the board state including updating and displaying the board and
# checking for winning conditions.

class Board:

    # Initializes the board, takes in two parameters (rows, cols) that
    # define the board size.
    def __init__(self, rows, cols):
        # Set the board size
        self.num_rows = rows
        self.num_cols = cols

        # Set the labels for the rows and columns
        self.row_labels = ['f', 'e', 'd', 'c', 'b', 'a']
        self.col_labels = [str(i) for i in range(1, self.num_cols + 1)]

        # Set the number of tokens per column to 0
        self.num_tokens_per_col = {col: 0 for col in range(1, self.num_cols + 1)}

        # Set each space in the game board to an empty space
        self.game_board = []
        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                row.append(' ')
            self.game_board.append(row)

    # Updates the game board with a player's token at their chosen location.
    # Tracks the number of tokens in each column.
    def UpdateBoard(self, player_choice, player_token):
        # Board[0][0] is at the top left of the game board, so the value
        # in 'row' is inverted
        row = self.num_tokens_per_col[player_choice]

        # To fix 'row', subtract from 1 then from the total rows on the board
        # Subtract 1 from player choice because lists are 0-indexed
        self.game_board[self.num_rows - 1 - row][player_choice - 1] = player_token

        # Update the number of entries by 1
        self.num_tokens_per_col[player_choice] = self.num_tokens_per_col[player_choice] + 1

    # Displays the game board in the current state.
    def DisplayBoard(self):
        # Print the vertical axis labels and the game board
        for i in range(self.num_rows):
            print(' ' * 2, end='')
            print('-' * 29)
            print(self.row_labels[i], end=' | ')
            print(' | '.join(self.game_board[i]), end='')
            print(' |')

        # print the horizontal axis labels
        print(' ' * 2, end='')
        print('-' * 29)
        print(' ' * 4, end='')
        print('   '.join(self.col_labels))

    # Checks if there are no more empty spaces on the board.
    # Returns a boolean value.
    def IsBoardFull(self):
        for num_tokens in self.num_tokens_per_col.values():
            if num_tokens != self.num_rows:
                return False
        return True

    # Checks the board to determine if there are 4 of the same tokens in a row
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
        # Check for up-right diagonal
        if (self.NumAdjacentTokens(player_token, start_row, start_col, 1, 1) +
            self.NumAdjacentTokens(player_token, start_row, start_col, -1, -1)) >= 3:
            return True
        # Check for down-right diagonal
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

                # Increase the number of consecutive tokens found, otherwise return the number of tokens
                if self.game_board[row_index][col_index] == player_token:
                    count += 1
                else:
                    break

            return count
        # Function reached the end of the board before 3 matching tokens were found
        except IndexError:
            return count
