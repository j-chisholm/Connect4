GAME_BOARD = []

def InitializeGameBoard():
    # Initialize a 6x7 game board and set each position to a single space
    for i in range(6):
        row = []
        for j in range(7):
            row.append(' ')
        GAME_BOARD.append(row)

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

def GetUserInput(current_player):
    # TODO: Function is incomplete. Validate that the chosen column is not full.
    # Prompt the user for an input and validate it against the current board state
    is_input_valid = False
    while not is_input_valid:
        print(f"\nPlayer {current_player}'s turn...")
        player_input = input("Which column will you place your piece?: ")
        try:
            player_input = int(player_input)
            if player_input not in range(1, 8):
                print("Sorry, that input is not in the range 1-7.\nPlease try again!")
            else:
                is_input_valid = True
        except ValueError:
            print("That is not a number, please try again!")

    return is_input_valid

def main():
    InitializeGameBoard()
    DisplayGameBoard()

    is_game_over = False
    current_player = 1

    while not is_game_over:
        pass

main()
