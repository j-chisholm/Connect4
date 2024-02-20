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
        ai_input = int(random.randint(1, NUM_COLS))
        if num_tokens_per_col[ai_input] < NUM_ROWS:
            break

    return ai_input

# Prompts the player for an input and returns it if it is valid
def GetPlayerChoice(current_player):
    # Print instructions to the player
    print(f"\nPlayer {current_player}'s turn...")
    player_choice = input("Choose a column to drop your token: ")

    return int(player_choice)

# Validate user input against the current board state
def IsChoiceValid(player_choice, num_tokens_per_col):
    try:
        player_choice = int(player_choice)
        if player_choice not in range(1, NUM_COLS + 1):
            print("Sorry, that choice is not in the range 1-7.\nPlease try again!")
        # check if the the column is full
        elif num_tokens_per_col[player_choice] >= NUM_ROWS:
            print("\nThat column is full, please try again!")
            return False
        else:
            return True
    except ValueError:
        print("That is not a number, please try again!")
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
def CheckFourInARow(player_token, player_choice, num_tokens_per_col, game_board):
    start_row = num_tokens_per_col[player_choice] - 1
    start_col = player_choice - 1

# Checks for four in a row in a given direction. Parameters row_increment,
# col_increment can be passed -1, 0, 1 to dictate which direction the
# function checks for four in a row
def CheckForFourInDirection(player_token, start_row, start_col, row_increment, col_increment):
    pass

def main():
    game_board, num_tokens_per_col = InitializeGame()

    DisplayGameBoard(game_board)

    is_game_over = False
    current_player = '1'

    while not is_game_over:
        if current_player == '1':
            player_token = 'X'

            player_choice = GetPlayerChoice(current_player)

            # Continue to prompt user until they provide a valid move
            while not IsChoiceValid(player_choice, num_tokens_per_col):
                DisplayGameBoard(game_board)
                player_choice = GetPlayerChoice(current_player)

            game_board, num_tokens_per_col = UpdateGameBoard(player_choice, player_token,
                                                             game_board, num_tokens_per_col)
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

        DisplayGameBoard(game_board)

main()
