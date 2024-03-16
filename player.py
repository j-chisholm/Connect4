# Player Class
# This class represents a player. It manages information such as the
# player's name and game piece.
import random

class Player:
    def __init__(self, player_name, player_number, player_token):
        self.name = player_name
        self.number = player_number
        self.token = player_token
        self.selection = None

    # Generates a random move for the player
    def GenerateRandomMove(self, num_cols):
        self.selection = int(random.randint(1, num_cols))

    # Returns the player's name
    def GetPlayerName(self):
        return self.name

    # Returns the player's number (1 or 2)
    def GetPlayerNumber(self):
        return self.number

    # Returns the player's token (X or O)
    def GetPlayerToken(self):
        return self.token   
