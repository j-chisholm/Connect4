# AI Manager Class
# This class is responsible for analyzing the board (state) and
# determining the best move for the AI to take (action)

import torch
import pygame
import sys
import math
import random
from board import Board
from connect4_ui import Connect4UI

NUM_SIMULATIONS = 100  # Number of simulations to iterate through

C = 1.4  # UCB Constant

# Board size
ROWS = 6
COLS = 7

# Create a board object to simulate the game

_board = [[' ', 'X', 'X', 'X', 'X', ' ', 'X'],
          [' ', 'O', 'X', 'O', 'X', ' ', 'O'],
          ['X', 'O', 'X', 'O', 'X', ' ', 'X'],
          ['O', 'X', 'O', 'X', 'O', ' ', 'X'],
          ['X', 'X', 'O', 'X', 'X', 'O', 'X'],
          ['X', 'O', 'O', 'X', 'X', 'X', 'O']]

board_manager = Board(ROWS, COLS, _board)
ui_manager = Connect4UI(ROWS, COLS)

# Returns the other player's piece
def OtherPlayer(curr_player):
    if curr_player == 'X':
        return 'O'
    else:
        return 'X'

def dummy_model_predict(board):
    value_head = 0.5  # Expected, estimated outcome of a given action
    policy_head = [0.5, 0, 0, 0, 0, 0.5, 0]  # Predicts the probability distribution for the possible actions
    return value_head, policy_head

# Calculate the UCB score using the general formula
def UCBScore(parent, child, c=1.4):
    # Check the number of times the child has been visited, this prevents div by 0
    if child.visits == 0:
        return float('inf')  # Returns a high number to prioritize unexplored child nodes

    # Calculate the UCB
    exploration_term = c * math.sqrt(math.log(parent.visits) / child.visits)
    ucb_score = child.value + exploration_term

    return ucb_score

class Node:
    # __init_ method is called at object instantiation
    def __init__(self, prob, player, board_state):
        self.prev_prob = prob  # previous probability predicted by network
        self.curr_player = player  # current player as the player's piece
        self.curr_board = board_state  # current board state

        self.children = {}  # initialize an empty dictionary of children nodes
        self.value = 0  # value of the node
        self.visits = 0  # number of times this node has been visited

    # Expands the node into children nodes
    def Expand(self, col_probs):  # col_probs = list containing the probability of each column being selected
        for choice, probability in enumerate(col_probs):

            # Expand the node if it has a non-zero probability of being selected
            if probability > 0:
                # Simulate the board state for this choice (column)
                board_manager.UpdateBoard(choice + 1, self.curr_player, self.curr_board)
                next_board_state = board_manager.GetGameBoard()

                # Create children nodes from this node
                self.children[choice] = Node(probability, OtherPlayer(self.curr_player), next_board_state)

    # Selects the next child node
    def SelectChild(self):
        max_score = -999  # Arbitrarily low max score
        best_choice = None
        best_child = None

        for choice, child in self.children.items():
            score = UCBScore(self, child)

            if score > max_score:
                best_choice = choice
                best_child = child
                max_score = score

        return best_choice, best_child

# Initialize the root node
root = Node(None, "X", _board)

# Expand the root
value, col_probability = dummy_model_predict(_board)
root.Expand(col_probability)

# Iterate over the simulations
for sim in range(NUM_SIMULATIONS):
    node = root  # Copy the root node into a new node
    search_path = [node]  # Create a search path to append each node to

    # Continue selecting the next child until we reach a leaf node
    # Leaf nodes describe a state at the end of a branch in a search tree. Often times leaf nodes are terminal nodes.
    while len(node.children) > 0:
        choice, node = node.SelectChild()
        search_path.append(node)

    value = None

    # Calculate value once a leaf node is reached
    choice += 1  # Account for 0-indexing
    if board_manager.IsBoardFull(node.curr_board):  # Game ends in a draw
        value = 0
    if board_manager.CheckFourInARow(node.curr_player, choice, node.curr_board):  # Current player would win
        value = 1
    if board_manager.CheckFourInARow(OtherPlayer(node.curr_player), choice, node.curr_board): # Other player would win
        value = -1

    if value is None:
        value, col_probability = dummy_model_predict(node.curr_board)
        node.Expand(col_probability)

    for node in search_path:
        node.value += value
        node.visits += 1

print(root.children[0].value)
print(root.children[5].value)

'''ui_manager.InitWindow()
while True:
    ui_manager.DrawBoardUI(root.children[5].curr_board)

    for event in pygame.event.get():
        # Quit if the 'x' button is clicked
        if event.type == pygame.QUIT:
            sys.exit()'''
