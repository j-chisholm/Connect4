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

    # Check for four in a row to the right
    if IsFourInDirection(game_board, player_token, start_row, start_col, 0, 1):
        return True

# Checks for four in a row in a given direction. Parameters row_increment,
# col_increment can be passed -1, 0, 1 to dictate which direction the
# function checks for four in a row
def IsFourInDirection(game_board, player_token, start_row, start_col, row_increment, col_increment):
    row_index = start_row
    col_index = start_col

    # Try block catches the instance where the function searches out of bounds for a player token
    try:
        # Only checks the next 3 spaces in a given direction,
        # no need to check that the player's current move matches their token
        for i in range(3):
            # Move to the next space in the specified direction
            row_index += row_increment
            col_index += col_increment

            # Return function execution to the main function after finding a different token before
            # 3 matching tokens have been found
            if game_board[row_index][col_index] != player_token:
                return False
    # Function reached the end of the board before 3 matching tokens were found
    except IndexError:
        return False

    # Program execution can only reach this line via finding 4 matching tokens in a row
    return True

def main():
    game_board, num_tokens_per_col = InitializeGame()

    DisplayGameBoard(game_board)

    is_game_over = False
    current_player = '1'

    while not is_game_over:
        if current_player == '1':
            player_token = 'X'

            # Continue to prompt user until they provide a valid move
            while True:
                player_choice = GetPlayerChoice(current_player)

                if not IsChoiceValid(player_choice, num_tokens_per_col):
                    time.sleep(1.5)
                    DisplayGameBoard(game_board)
                else:
                    player_choice = int(player_choice)
                    break

            game_board, num_tokens_per_col = UpdateGameBoard(player_choice, player_token,
                                                             game_board, num_tokens_per_col)
            DisplayGameBoard(game_board)

            if CheckFourInARow(game_board, player_token, player_choice, num_tokens_per_col):
                print(f"\nPlayer {current_player} wins!")
                break
            # current_player = '2'
        else:
            print("Computer's turn...")
            time.sleep(2)
            player_token = 'O'
            UpdateGameBoard(GenerateAIMove(num_tokens_per_col), player_token, game_board, num_tokens_per_col)
            current_player = '1'

        if IsBoardFull(num_tokens_per_col):
            is_game_over = True
            print('DRAW!')

        # DisplayGameBoard(game_board)

main()
