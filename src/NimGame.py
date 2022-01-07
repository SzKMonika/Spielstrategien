import random

# -------------------- class NimGame --------------------
class NimGame:
    def __init__(self, player1, player2, sticks, maxTake= 3, lastOneLoses = True):
        self.__sticks = sticks
        self.__minTake = 1
        self.__maxTake = maxTake
        self.__lastOneLoses = lastOneLoses
        self.__playerCallback = (player1, player2)
        self.__nextPlayer = 1
        self.__nextMove = 0
        self.__moveRecords = []
    
    @property
    def sticks(self):
        return self.__sticks
        
    @property
    def minTake(self):
        return self.__minTake
    
    @property
    def maxTake(self):
        return self.__maxTake
    
    @property
    def nextMove(self):
        return self.__nextMove
    
    def play(self):
        """Startet das Spiel und ruft alternierend beide Spieler-Strategien auf, bis eine gewinnt."""
        try:
            while self.__sticks > 0:
                self.__nextMove += 1
                take = self.__playerCallback[self.__nextPlayer-1](self)
                self.checkMove(take)
                self.__sticks = self.__sticks - take
                self.__recordState((self.__nextMove, self.__nextPlayer, take, self.__sticks))
                self.__nextPlayer = self.__nextPlayer%2+1
            self.__nextPlayer = -self.__nextPlayer if self.__lastOneLoses else -(self.__nextPlayer%2+1)
            self.__recordState((self.__nextMove, self.__nextPlayer, None, None))
        except ValueError as e:
            self.__recordState((self.__nextMove, -(self.__nextPlayer%2+1), take, self.__sticks))
        
    def checkMove(self, take):
        """Prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht."""
        if self.__minTake > take or min(self.__maxTake, self.__sticks) < take:
            raise ValueError("wollte " + str(take) + " statt zwischen " + str(self.__minTake) + " und " + str(min(self.__maxTake, self.__sticks)) + " nehmen.")

    def __recordState(self, state):
        """Speichert den Zug und den Spielstand ab um am Ende des Spiels den Spielablauf sehen zu können."""
        self.__moveRecords.append(state)

    def stateToString(self, state):
        """Gibt den Spielstand nach einem Zug in kompakter/ausdruckbarer Form zurück."""
        s = ""
        if (state[1] >= 0):
            s += "({:2d}/{:d}): {:2d} -{:2d} => {:2d}".format(state[0], state[1], state[2]+state[3], state[2], state[3])
        else:
            s += "  Spieler {:d} gewinnt nach {:d} Zügen!".format(-state[1], state[0])
            if (state[2] != None):
                s += " Grund: Falscher Zug ({:d}) des anderen Spielers.".format(state[2])
        return s

    def printAllStates(self):
        """Gibt alle Züge zurück bzw. in kompakter Form aus."""
        for state in self.__moveRecords:
            print(self.stateToString(state))

# -------------------- Human player callback --------------------   
def human(game):
    """Ein Callback für einen menschlichen Spieler, der den Benutzer um ihren Zug fragt."""
    n = 0
    while n < game.minTake or n > game.maxTake:
        try:
            n = int(input(str(game.nextMove) + ". Zug kommt und es sind noch " + str(game.sticks) + " Sticks da. Wie viel nimmst du weg?\n"
                + "Bitte eine ganze Zahl zwischen " + str(game.minTake) + " und " + str(game.maxTake) + " angeben!"))
        except ValueError:
            n = 0
    return n

# -------------------- Computer player callbacks --------------------   
def computer1(game):
    """Callback für einen dummen Computerspieler."""
    return random.randint(game.minTake, min(game.maxTake, game.sticks))

def computer2(game):
    """Callback für den optimalen Computerspieler."""
    nextTake = (game.sticks - 1) % (game.minTake + game.maxTake)
    return (nextTake if nextTake > 0 else 1)
