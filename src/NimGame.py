from Game import Game
import random

# -------------------- class NimGame --------------------
class NimGame(Game):
    def __init__(self, player1, player2, sticks, player1name = "Spieler 1", player2name = "Spieler 2", maxTake = 3, lastOneLoses = True):
        super(NimGame, self).__init__(player1, player2, player1name, player2name)
        self.__sticks = sticks
        self.__minTake = 1
        self.__maxTake = maxTake
        self.__lastOneLoses = lastOneLoses
    
    @property
    def gamePanel(self):
        return self.__sticks
        
    @property
    def minTake(self):
        return self.__minTake
    
    @property
    def maxTake(self):
        return self.__maxTake
    
    def checkMove(self, move):
        """Prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht."""
        if not isinstance(move, int):
            raise ValueError("Es muss eine ganze Zahl angegeben werden!")
        if self.__minTake > move or min(self.__maxTake, self.__sticks) < move:
            raise ValueError("Ungültiger Zug " + str(move) + " statt zwischen " + str(self.__minTake) + " und " + str(min(self.__maxTake, self.__sticks)) + "!")

    def _doMove(self, move):
        """Macht den aktuellen Zug und gibt zurück welcher Spieler als nächster kommt."""
        self.__sticks = self.__sticks - move
        return (self.nextPlayer % 2 + 1)

    def _checkEnd(self, move):
        """Gibt an ob das Spiel mit unentschieden beendet ist (0) oder ein Spieler gewonnen hat (1 oder 2), oder noch nicht beendet ist (None)"""
        return None if self.__sticks > 0 else (self.nextPlayer%2+1) if self.__lastOneLoses else self.nextPlayer

# -------------------- Computer player callbacks --------------------   
def Nim_L1(game):
    """Callback für einen dummen Computerspieler."""
    return random.randint(game.minTake, min(game.maxTake, game.gamePanel))

def Nim_L3(game):
    """Callback für den optimalen Computerspieler."""
    nextTake = (game.gamePanel - 1) % (game.minTake + game.maxTake)
    return (nextTake if nextTake > 0 else 1)
