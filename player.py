# Player Class
# This class represents a player. It manages information such as the
# player's name and game piece.

class Player:
    # __init__ method called at object instantiation
    def __init__(self, player_name, player_number, player_token):
        self.name = player_name
        self.number = player_number
        self.token = player_token

        self.isHuman = False  # Designates the instance as a human (True) or a computer (False)

    # Returns the player's name
    def GetPlayerName(self):
        return self.name

    # Assigns the player's name
    def SetPlayerName(self, player_name):
        self.name = player_name

    # Returns the player's token (X or O)
    def GetPlayerToken(self):
        return self.token

    # Assigns the player's token
    def SetPlayerToken(self, player_token):
        self.token = player_token

    # Designates this object as a human-controlled player
    def SetAsHuman(self):
        self.isHuman = True

    # Designates this object as a computer-controlled player
    def SetAsComputer(self):
        self.isHuman = False
