# Player Class
# This class represents a player. It manages information such as the
# player's name and game piece.

class Player:
    def __init__(self, player_name, player_number, player_token):
        self.name = player_name
        self.number = player_number
        self.token = player_token

        self.is_my_turn = False

    # Swaps the player's turn to true or false
    def SwapTurn(self):
        if self.is_my_turn:
            self.is_my_turn = False
        else:
            self.is_my_turn = True

    # Returns the player's name
    def GetPlayerName(self):
        return self.name

    # Assigns the player's name
    def SetPlayerName(self, player_name):
        self.name = player_name

    # Returns the player's number
    def GetPlayerNumber(self):
        return self.number

    # Assigns the player's number (1 or 2)
    def SetPlayerNumber(self, player_number):
        self.number = player_number

    # Returns the player's token (X or O)
    def GetPlayerToken(self):
        return self.token

    # Assigns the player's token
    def SetPlayerToken(self, player_token):
        self.token = player_token

    # Returns a boolean that represents whether it is the player's turn
    def IsCurrentPlayer(self):
        return self.is_my_turn

    # Sets the player as the current player
    def SetCurrentPlayer(self):
        self.is_my_turn = True

