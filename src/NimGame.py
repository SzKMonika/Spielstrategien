from Game import Game
import random

# -------------------- class NimGame --------------------
class NimGame(Game):
    """Das ist ein konkretes Spiel (Game), wo die zwei Spieler abwechselnd 1 bis 3 (maxTake) Objekte wegnehmen von beim Spielbeginn 'sticks' Anzahl an Objekten.
    Gewonnen hat beim Standardspiel (lastOneLoses=False) derjenige, der das letzte Stück nimmt, bei der Misère-Variante (lastOneLoses=True) verliert dieser.
    Unten werden nur die Nim-spezifische Argumente und Attribute aufgeführt, für die sonstigen bitte im Game schauen.

    Args:
        sticks (int): Anzahl der Objekte beim Spielbeginn.
        maxTake (int): Maximale Anzahl der Objekte die in einem Zug weggenommen werden können.
        lastOneLoses (bool): Gibt an, welche Variante gespielt wird. False bedeutet die Standard-Variante, True bedeutet die Misère-Variante.

    Attributes:
        __sticks (int): Die aktuelle Anzahl der Objekte, am Anfang 'sticks'.
        __maxTake (int): Der als 'maxTake' angegebene Wert.
        __lastOneLoses (bool): Die Spielvariante, die als 'lastOneLoses' angegeben wurde.
    """
    def __init__(self, player1, player2, sticks = 15, maxTake = 3, lastOneLoses = True):
        super(NimGame, self).__init__(player1, player2)
        self.__sticks = sticks
        self.__maxTake = maxTake
        self.__lastOneLoses = lastOneLoses
    
    @property
    def gamePanel(self):
        return self.__sticks
    
    @property
    def maxTake(self):
        """Maximale Anzahl der Objekte, die in einem Zug weggenommen werden können."""
        return self.__maxTake
    
    @property
    def lastOneLoses(self):
        """Gibt an, welche Variante gespielt wird. False bedeutet die Standard-Variante, True bedeutet die Misère-Variante."""
        return self.__lastOneLoses

    def checkMove(self, move):
        if not isinstance(move, int):
            raise ValueError("Es muss eine ganze Zahl angegeben werden!")
        if 1 > move or min(self.__maxTake, self.__sticks) < move:
            raise ValueError("Ungültiger Zug " + str(move) + " statt zwischen 1 und " + str(min(self.__maxTake, self.__sticks)) + "!")

    def _doMove(self, move):
        self.__sticks = self.__sticks - move
        return (self.nextPlayer%2 + 1)

    def _checkEnd(self, move):
        return None if self.__sticks > 0 else (self.nextPlayer%2 + 1) if self.__lastOneLoses else self.nextPlayer

# -------------------- Computer Strategien --------------------   
def Nim_L1(game):
    """Strategie für einen dummen Computerspieler."""
    return random.randint(1, min(game.maxTake, game.gamePanel))

def Nim_L2(game):
    """Strategie für einen mittelmässigen Computerspieler."""
    last = (1 if game.lastOneLoses else 0)

    if game.gamePanel <= game.maxTake + last:
        return max(1, game.gamePanel - last)
    elif game.gamePanel <= 2*game.maxTake + 1 + last:
        return max(1, game.gamePanel - (game.maxTake + 1 + last))
    else:
        return random.randint(1, min(game.maxTake, game.gamePanel))

def Nim_L3(game):
    """Strategie für den optimalen Computerspieler."""
    last = (1 if game.lastOneLoses else 0)
    nextTake = (game.gamePanel - last) % (game.maxTake + 1)
    return (nextTake if nextTake > 0 else 1)
