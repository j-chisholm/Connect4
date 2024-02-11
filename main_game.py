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

def main():
    InitializeGameBoard()
    DisplayGameBoard()

    is_game_over = False

main()
