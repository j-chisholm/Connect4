import random
import time

# List variable to track the current board state
GAME_BOARD = []
# Initialize dict variable to track the number of entries to each column
COL_ENTRIES = {col: 0 for col in range(1, 8)}

# Initialize a 6x7 game board and set each position to a single space
def InitializeGameBoard():
    for i in range(6):
        row = []
        for j in range(7):
            row.append(' ')
        GAME_BOARD.append(row)

# Displays the current state of the game board
def DisplayGameBoard():
    # Print the game board to the screen along with the row and col labels
    row_labels = ['f', 'e', 'd', 'c', 'b', 'a']
    col_labels = [str(i) for i in range(1, 8)]

    # Print the vertical axis labels and the game board
    for i in range(6):
        print(' ' * 2, end='')
        print('-' * 29)
        print(row_labels[i], end=' | ')
        print(' | '.join(GAME_BOARD[i]), end='')
        print(' |')

    # print the horizontal axis labels
    print(' ' * 2, end='')
    print('-' * 29)
    print(' ' * 4, end='')
    print('   '.join(col_labels))

# Generates a random, valid input for the AI opponent
def GenerateAIMove():
    while True:
        ai_input = int(random.randint(1, 7))
        if COL_ENTRIES[ai_input] < 6:
            break

    return ai_input

# Prompts the player for an input and returns it if it is valid
def GetPlayerInput(current_player):
    # Print instructions to the player
    print(f"\nPlayer {current_player}'s turn...")
    player_input = input("Choose a column to drop your piece: ")

    # Validates the user's input, if invalid, prompt the user for a new input
    while not IsInputValid(player_input):
        DisplayGameBoard()
        print(f"\nPlayer {current_player}'s turn...")
        player_input = input("Choose a column to drop your piece: ")

    return int(player_input)

# Validate user input against the current board state
def IsInputValid(player_input):
    try:
        player_input = int(player_input)
        if player_input not in range(1, 8):
            print("Sorry, that input is not in the range 1-7.\nPlease try again!")
        # check if the the column is full
        elif COL_ENTRIES[player_input] >= 6:
            print("Your chosen column is full, please try again!")
            return False
        else:
            return True
    except ValueError:
        print("That is not a number, please try again!")
        return False
    except OverflowError:
        print("That number is too large, please try again!")

# Places the player's piece in their chosen column
def UpdateGameBoard(col, player_piece):
    row = COL_ENTRIES[col]
    GAME_BOARD[5 - row][col-1] = player_piece

    # Update the number of entries by 1 if the column is not full
    COL_ENTRIES[col] = COL_ENTRIES[col] + 1

# Checks if any column in the game board is not full
def IsBoardFull():
    for num_entries in COL_ENTRIES.values():
        if num_entries != 7:
            return False
    return True

def main():
    InitializeGameBoard()
    DisplayGameBoard()

    is_game_over = False
    current_player = '1'
    player_piece = 'X'

    while not is_game_over:
        if current_player == '1':
            player_piece = 'X'
            player_input = GetPlayerInput(current_player)
            UpdateGameBoard(player_input, player_piece)
            current_player = '2'
        else:
            print("Computer's turn...")
            time.sleep(2)
            player_piece = 'O'
            UpdateGameBoard(GenerateAIMove(), player_piece)
            current_player = '1'

        if IsBoardFull():
            is_game_over = True
            print('DRAW!')

        DisplayGameBoard()

main()
