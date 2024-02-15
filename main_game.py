GAME_BOARD = []

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

# Prompts the player for an input and returns it if it is valid
def GetPlayerInput(current_player):
    # Print instructions to the player
    print(f"\nPlayer {current_player}'s turn...")
    player_input = input("Which column will you place your piece?: ")

    # Validates the user's input, if invalid, prompt the user for a new input
    while not IsInputValid(player_input):
        player_input = input("Which column will you place your piece?: ")

    return int(player_input)

# Validate user input against the current board state
def IsInputValid(player_input):
    # TODO: Function is incomplete. Validate that the chosen column is not full.
    try:
        player_input = int(player_input)
        if player_input not in range(1, 8):
            print("Sorry, that input is not in the range 1-7.\nPlease try again!")
        else:
            return True
    except ValueError:
        print("That is not a number, please try again!")
        return False
    except OverflowError:
        print("That number is too large, please try again!")

# Places the player's piece in their chosen column
def UpdateGameBoard(col, player_piece):
    # Ensures player choice is within list bounds (0-indexed)
    col = col - 1

    # Checks the column from the bottom up to locate an empty space and places
    # player's piece in that space
    for i in range(5, -1, -1):
        if GAME_BOARD[i][col] == ' ':
            GAME_BOARD[i][col] = player_piece
            break

def main():
    InitializeGameBoard()
    DisplayGameBoard()

    is_game_over = False
    current_player = '1'
    player_piece = 'X'

    while not is_game_over:
        if current_player == '1':
            player_piece = 'X'
        else:
            player_piece = 'O'

        player_input = GetPlayerInput(current_player)

        UpdateGameBoard(player_input, player_piece)
        DisplayGameBoard()

main()
