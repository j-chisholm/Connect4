import random
import time

# Initialize constant variables
NUM_ROWS = 6
NUM_COLS = 7

# Initialize a 6x7 game board and set each position to a single space
# Initialize a dictionary to track the number of entries to each column
def InitializeGame():
    num_tokens_per_col = {col: 0 for col in range(1, NUM_COLS + 1)}

    board = []
    for i in range(NUM_ROWS):
        row = []
        for j in range(NUM_COLS):
            row.append(' ')
        board.append(row)

    return board, num_tokens_per_col

# Displays the current state of the game board
def DisplayGameBoard(game_board):
    # Print the game board to the screen along with the row and col labels
    row_labels = ['f', 'e', 'd', 'c', 'b', 'a']
    col_labels = [str(i) for i in range(1, NUM_COLS + 1)]

    # Print the vertical axis labels and the game board
    for i in range(NUM_ROWS):
        print(' ' * 2, end='')
        print('-' * 29)
        print(row_labels[i], end=' | ')
        print(' | '.join(game_board[i]), end='')
        print(' |')

    # print the horizontal axis labels
    print(' ' * 2, end='')
    print('-' * 29)
    print(' ' * 4, end='')
    print('   '.join(col_labels))

# Generates a random, valid input for the AI opponent
def GenerateAIMove(num_tokens_per_col):
    while True:
        ai_choice = int(random.randint(1, NUM_COLS))
        if num_tokens_per_col[ai_choice] < NUM_ROWS:
            break

    return ai_choice

# Prompts the player for an input and returns it if it is valid
def GetPlayerChoice(current_player):
    # Print instructions to the player
    print(f"\nPlayer {current_player}'s turn...")
    player_choice = input("Enter a column (1-7) to to drop your token: ")

    return player_choice

# Validate user input against the current board state
def IsChoiceValid(player_choice, num_tokens_per_col):
    if player_choice == '':
        print("\nNo value entered.\nPlease try again!")
        return False
    try:
        player_choice = int(player_choice)
        if player_choice not in range(1, NUM_COLS + 1):
            print("\nSorry, that choice is not in the range 1-7.\nPlease try again!")
        # check if the column is full
        elif num_tokens_per_col[player_choice] >= NUM_ROWS:
            print("\nThat column is full, please try again!")
            return False
        else:
            return True
    except ValueError:
        print("\nThat is not a number, please try again!")
        return False
    except OverflowError:
        print("That number is too large, please try again!")

# Places the player's token in their chosen column
def UpdateGameBoard(col, player_token, game_board, num_tokens_per_col):
    row = num_tokens_per_col[col]
    game_board[NUM_ROWS - 1 - row][col-1] = player_token

    # Update the number of entries by 1 if the column is not full
    num_tokens_per_col[col] = num_tokens_per_col[col] + 1

    return game_board, num_tokens_per_col

# Checks if any column in the game board is not full
def IsBoardFull(num_tokens_per_col):
    for num_tokens in num_tokens_per_col.values():
        if num_tokens != NUM_ROWS:
            return False
    return True

# Checks the board to determine if there are 4 of the same tokens in a row
def CheckFourInARow(game_board, player_token, player_choice, num_tokens_per_col):
    start_row = NUM_ROWS - num_tokens_per_col[player_choice]
    start_col = player_choice - 1

    # Check for four in a row horizontally
    if (NumAdjacentTokens(game_board, player_token, start_row, start_col, 0, 1) +
            NumAdjacentTokens(game_board, player_token, start_row, start_col, 0, -1)) >= 3:
        return True
    # Check for four in a row vertically
    if (NumAdjacentTokens(game_board, player_token, start_row, start_col, 1, 0) +
            NumAdjacentTokens(game_board, player_token, start_row, start_col, -1, 0)) >= 3:
        return True
    # Check for up-right diagonal
    if (NumAdjacentTokens(game_board, player_token, start_row, start_col, 1, 1) +
            NumAdjacentTokens(game_board, player_token, start_row, start_col, -1, -1)) >= 3:
        return True
    # Check for down-right diagonal
    if (NumAdjacentTokens(game_board, player_token, start_row, start_col, -1, 1) +
            NumAdjacentTokens(game_board, player_token, start_row, start_col, 1, -1)) >= 3:
        return True

    # If execution reaches this line, 4 in a row was not found
    return False

# Checks for adjacent tokens in a single direction.
# Returns the number of tokens found. Parameters row_increment, col_increment can be passed -1, 0, 1
# to dictate which direction the function checks for adjacent matching tokens
def NumAdjacentTokens(game_board, player_token, start_row, start_col, row_increment, col_increment):
    row_index = start_row
    col_index = start_col
    count = 0

    # Try block catches the instance where the function searches out of bounds for a player token
    try:
        # Only checks the next 3 spaces in a given direction,
        # no need to check that the player's current move matches their token
        for i in range(3):
            # Move to the next adjacent space
            row_index += row_increment
            col_index += col_increment

            # Increase the number of consecutive tokens found, otherwise return the number of tokens
            if game_board[row_index][col_index] == player_token:
                count += 1
            else:
                break

        return count
    # Function reached the end of the board before 3 matching tokens were found
    except IndexError:
        return count

def main():
    game_board, num_tokens_per_col = InitializeGame()
    DisplayGameBoard(game_board)

    is_game_over = False
    current_player = '1'

    while not is_game_over:
        # Player 1's turn
        if current_player == '1':
            player_token = 'X'

            # Continue to prompt user until they provide a valid move
            while True:
                player_choice = GetPlayerChoice(current_player)

                if not IsChoiceValid(player_choice, num_tokens_per_col):
                    # Pause execution to allow player time to read on screen instructions
                    time.sleep(1.5)
                    DisplayGameBoard(game_board)

                # Player's move is valid and can be converted to INT
                else:
                    player_choice = int(player_choice)
                    break

            game_board, num_tokens_per_col = UpdateGameBoard(player_choice, player_token,
                                                             game_board, num_tokens_per_col)

            # Check if player's move resulted in 4 in a row
            if CheckFourInARow(game_board, player_token, player_choice, num_tokens_per_col):
                DisplayGameBoard(game_board)
                print(f"\nPlayer {current_player} wins!")
                break

            current_player = '2'
        else:
            print("Computer's turn...")
            time.sleep(1)

            player_token = 'O'
            player_choice = GenerateAIMove(num_tokens_per_col)

            UpdateGameBoard(player_choice, player_token, game_board, num_tokens_per_col)

            # Check if player's move resulted in 4 in a row
            if CheckFourInARow(game_board, player_token, player_choice, num_tokens_per_col):
                DisplayGameBoard(game_board)
                print(f"\nComputer wins!")
                break

            current_player = '1'

        DisplayGameBoard(game_board)

        # End the game if the board is full
        if IsBoardFull(num_tokens_per_col):
            is_game_over = True
            print('DRAW!')

    input("Press Enter to exit...")

main()
