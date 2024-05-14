# AI Manager Class
# Singleton
# This class is responsible for analyzing the board (state) and
# determining the best move for the AI to take (action)

import math
import copy
import random
import threading

class AIManager():
    instance = None

    # Ensure that only one instance of this class exists
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, rows, cols):
        self.num_rows = rows
        self.num_cols = cols

        self.ai_token = None
        self.opp_token = None

        # Init transposition table
        self.transposition_table = {}
        self.transposition_table_lock = threading.Lock()

        self.first_time = True
        self.complexity_score = 0

    # Generate a unique key for each board state and its mirrored alternatives
    def GenerateKeyForBoard(self, board):
        # Generate the original key
        original_key = ''.join(''.join(row) for row in board)
        mirrored_horizontally = self.MirrorBoardHorizontally(board)

        # Generate keys for mirrored states as well
        mirrored_horizontal_key = ''.join(''.join(row) for row in mirrored_horizontally)

        # Return the smallest key in lexicographical order
        return min(original_key, mirrored_horizontal_key)

    # Clear transposition table to save memory
    def ClearTranspositionTable(self):
        self.transposition_table.clear()

    # Determines whether a node is terminal
    def IsTerminalNode(self, board_manager):
        if (board_manager.IsBoardFull() or  # Draw
                self.HasPlayerWon(board_manager.GetGameBoard(), self.ai_token) or  # Current player wins
                self.HasPlayerWon(board_manager.GetGameBoard(), self.opp_token)):  # Opponent wins
            return True

        return False

    # Returns the opposite player's token
    def OtherPlayer(self, curr_player):
        return 'O' if curr_player == 'X' else 'X'

    def SetTokens(self, token, opp_token):
        self.ai_token = token
        self.opp_token = opp_token

    def MirrorBoardHorizontally(self, board):
        mirrored_board = [row[::-1] for row in board]
        return mirrored_board

    # Rates the board based on how many opportunities for success and failure are present
    def RateMove(self, game_board, token):
        score = 0

        # Center column
        center_column = list(game_board[i][self.num_cols // 2] for i in range(self.num_rows))
        center_count = center_column.count(token)
        score += center_count * 6

        #Define each direction to check in
        directions = [
            (1, 0),  # Vertical
            (0, 1),  # Horizontal
            (1, 1),  # Positive slope diagonal
            (-1, 1)  # Positive slop diagonal
        ]

        # Iterate over each position on the board
        for row in range(self.num_rows):
            for col in range(self.num_cols):

                # Check each direction
                for v, h in directions:
                    own_token_count = 0
                    opp_token_count = 0
                    empty_spaces = 0

                    # Check for ai tokens
                    # Check sections of four spaces long
                    for i in range(4):
                        r = row + i * v
                        c = col + i * h

                        # Check that we remain in the bounds of the board
                        if 0 <= r < self.num_rows and 0 <= c < self.num_cols:
                            if game_board[r][c] == token:
                                own_token_count += 1
                            elif game_board[r][c] == ' ':
                                empty_spaces += 1
                            else:
                                break

                    # Check for opp tokens
                    # Check sections of four spaces long
                    for i in range(4):
                        r = row + i * v
                        c = col + i * h

                        # Check that we remain in the bounds of the board
                        if 0 <= r < self.num_rows and 0 <= c < self.num_cols:
                            if game_board[r][c] == self.OtherPlayer(token):
                                opp_token_count += 1
                            elif game_board[r][c] == ' ':
                                empty_spaces += 1
                            else:
                                break

                    # Score each section
                    if own_token_count == 4:
                        score += 100
                    elif own_token_count == 3 and empty_spaces == 1:
                        score += 5
                    elif own_token_count == 2 and empty_spaces == 2:
                        score += 2

                    if opp_token_count == 3 and empty_spaces == 1:
                        score -= 4

        return score

    # Returns a list of valid moves
    def GetValidMoves(self, board_manager, token):
        # Get the center column index
        center_col = (self.num_cols // 2 + 1)

        # Store the columns into separate categories
        center_moves = []  # moves in the center column
        adjacent_moves = []  # moves in the columns next to the center
        outer_moves = []  # all other columns

        # Iterate through the columns and categorize the moves
        for col, num_tokens in board_manager.GetTokensPerColumn().items():
            if num_tokens < self.num_rows:
                if col == center_col:
                    center_moves.append(col)
                elif abs(col - center_col) == 1:
                    adjacent_moves.append(col)
                else:
                    outer_moves.append(col)

        # Combine moves in order of priority
        # After sorting, all_valid_moves will contain a list of moves that are not winning_moves, blocking_moves,
        # or losing_moves
        all_valid_moves = center_moves + adjacent_moves + outer_moves

        winning_moves = []  # stores moves that result in an ai win on the current turn
        blocking_moves = []  # stores moves that block the opponent from winning on the next turn
        losing_moves = []  # stores the moves that result in an opponent win on the following turn

        # Check the list of valid moves to see which results in a win on the ai's current turn
        for move in all_valid_moves:
            board_manager_copy = copy.deepcopy(board_manager)

            # Simulate ai making this move and check if it wins. Add to winning moves if it does
            board_manager_copy.UpdateBoard(move, token)
            if board_manager_copy.CheckFourInARow(token, move):
                winning_moves.append(move)
                all_valid_moves.remove(move)

        # Check the list of valid moves to see which prevent the opponent from winning. Add to blocking moves if it does
        for move in all_valid_moves:
            board_manager_copy = copy.deepcopy(board_manager)

            # Simulate the opponent making this move
            board_manager_copy.UpdateBoard(move, self.OtherPlayer(token))
            if board_manager_copy.CheckFourInARow(self.OtherPlayer(token), move):
                blocking_moves.append(move)
                all_valid_moves.remove(move)

        # Check the list valid moves to see which result in a win on the opp's next turn
        for move in all_valid_moves:
            board_manager_copy = copy.deepcopy(board_manager)

            # Simulate ai making this move
            board_manager_copy.UpdateBoard(move, token)

            # Check to make sure column is not full after ai's move
            if board_manager_copy.GetTokensPerColumn()[move] < self.num_rows:
                # Simulate opp's next move in the same column
                board_manager_copy.UpdateBoard(move, self.OtherPlayer(token))

                # Check if the opp wins from this move
                if board_manager_copy.CheckFourInARow(self.OtherPlayer(token), move):
                    losing_moves.append(move)
                    all_valid_moves.remove(move)

        return winning_moves + blocking_moves, losing_moves, all_valid_moves

    # Defines the MiniMax algorithm
    def MiniMax(self, board_manager, depth, alpha, beta, maximizing_player, token):
        best_moves, losing_moves, other_moves = self.GetValidMoves(board_manager, token)
        # AI should only consider the best moves unless only unfavorable moves are left
        if len(best_moves) > 0:
            moves_list = best_moves
        elif len(other_moves) > 0:
            moves_list = other_moves
        else:
            moves_list = losing_moves

        curr_board = board_manager.GetGameBoard()

        # Convert the board to a key
        board_key = self.GenerateKeyForBoard(curr_board)

        # Check if the current state has already been evaluated
        with self.transposition_table_lock:
            if board_key in self.transposition_table:
                # Return the best score and column from the table for that board
                return self.transposition_table[board_key]

        if self.IsTerminalNode(board_manager):  # Reached a terminal node
            if self.HasPlayerWon(curr_board, self.ai_token):
                return math.inf, None
            elif self.HasPlayerWon(curr_board, self.opp_token):
                return -math.inf, None
            else:  # No more valid moves, the game is over
                return 0, None
        elif depth == 0:  # Depth is 0, return the heuristic value of the board
            return self.RateMove(curr_board, self.ai_token), None

        if maximizing_player:
            best_score = -math.inf  # Set an extremely small value for max comparison
            best_column = random.choice(moves_list)

            for col in moves_list:
                board_manager_copy = copy.deepcopy(board_manager)
                board_manager_copy.UpdateBoard(col, self.ai_token)
                score = self.MiniMax(board_manager_copy, depth-1, alpha, beta, False,
                                     self.opp_token)[0]

                if score > best_score:
                    best_score = score
                    best_column = col

                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break

                # Store the best value and column for the board in the table
                with self.transposition_table_lock:
                    self.transposition_table[board_key] = (best_score, best_column)

            return best_score, best_column
        else:  # Minimizing player
            best_score = math.inf  # Set an extremely large value for min comparison
            best_column = random.choice(moves_list)

            for col in moves_list:
                board_manager_copy = copy.deepcopy(board_manager)
                board_manager_copy.UpdateBoard(col, self.opp_token)
                score = self.MiniMax(board_manager_copy, depth-1, alpha, beta, True,
                                     self.ai_token)[0]

                if score < best_score:
                    best_score = score
                    best_column = col

                beta = min(beta, best_score)
                if alpha >= beta:
                    break

                # Store the best value and column for the board in the table
                with self.transposition_table_lock:
                    self.transposition_table[board_key] = (best_score, best_column)

            return best_score, best_column

    # Determines if the provided player has 4 pieces in a row
    def HasPlayerWon(self, game_board, token):
        token_count = 0

        # Define each direction to check in
        directions = [
            (1, 0),  # Vertical
            (0, 1),  # Horizontal
            (1, 1),  # Positive slope diagonal
            (-1, 1)  # Positive slop diagonal
        ]

        # Iterate over each position on the board
        for row in range(self.num_rows):
            for col in range(self.num_cols):

                # Check each direction
                for v, h in directions:

                    # Check sections of four spaces long
                    for i in range(4):
                        r = row + i * v
                        c = col + i * h

                        # If statement ensures the check remains within the bounds of the board
                        if 0 <= r < self.num_rows and 0 <= c < self.num_cols:
                            if game_board[r][c] == token:
                                token_count += 1
                            else:
                                break

                    # Connect 4 is found
                    if token_count == 4:
                        return True

                    token_count = 0

        # No connect 4 found, return false
        return False

    # Determines board complexity
    # Takes into account how full the board is, and potential winning moves for the ai and opponent
    def DetermineBoardComplexity(self, board_manager):
        curr_board = board_manager.GetGameBoard()
        tokens_per_col = board_manager.GetTokensPerColumn()

        board_complexity = 0

        # Calculate how full the board is, fuller board = more complex board
        total_pieces = sum(tokens_per_col.values())
        board_fullness = total_pieces / (self.num_rows * self.num_cols)  # pieces on the board to total spaces
        board_complexity += board_fullness * 10  # Constant is the weight of the board fullness in the complexity score

        # Determine how many winning moves are available for the ai and opponent
        ai_winning_moves = self.FindNumberOfPotentialWins(curr_board, self.ai_token)
        opp_winning_moves = self.FindNumberOfPotentialWins(curr_board, self.opp_token)

        # Calculate the added complexity of for the number of winning moves on both sides
        board_complexity += (ai_winning_moves * 2)  # Constant is the weight of the ai's winning moves
        board_complexity += (opp_winning_moves * 3)  # Constant is the weight of the opp's winning moves

        print(board_complexity)
        return board_complexity

    # Finds the number of potential winning moves for the provided token
    def FindNumberOfPotentialWins(self, game_board, token):
        num_potential_wins = 0

        # Define each direction to check in
        directions = [
            (1, 0),  # Vertical
            (0, 1),  # Horizontal
            (1, 1),  # Positive slope diagonal
            (-1, 1)  # Positive slop diagonal
        ]

        # Iterate over each position on the board
        for row in range(self.num_rows):
            for col in range(self.num_cols):

                # Check each direction
                for v, h in directions:
                    token_count = 0
                    empty_space_count = 0
                    winning_position = True

                    # Check sections of four spaces long
                    for i in range(4):
                        r = row + i * v
                        c = col + i * h

                        # If statement ensures the check remains within the bounds of the board
                        if 0 <= r < self.num_rows and 0 <= c < self.num_cols:
                            if game_board[r][c] == token:
                                token_count += 1
                            elif game_board[r][c] == ' ':
                                empty_space_count += 1
                            else:
                                winning_position = False
                                break
                        else:
                            winning_position = False
                            break

                    # Winning move is found
                    if token_count == 3 and empty_space_count == 1 and winning_position:
                        num_potential_wins += 1

        return num_potential_wins
