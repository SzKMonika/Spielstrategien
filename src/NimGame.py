import random

# -------------------- class NimGame --------------------
class NimGame:
    def __init__(self, player1, player2, sticks, maxTake):
        self.__sticks = sticks
        self.__minTake = 1
        self.__maxTake = maxTake
        self.__player = (player1, player2)
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
                take = self.__player[self.__nextPlayer-1](self)
                self.checkMove(take)
                self.__sticks = self.__sticks - take
                self.__recordState((self.__nextMove, self.__nextPlayer, take, self.__sticks))
                self.__nextPlayer = (self.__nextPlayer%2+1)
            self.__recordState((self.__nextMove, -self.__nextPlayer, None, None))
        except ValueError as e:
            self.__recordState((self.__nextMove, -(self.__nextPlayer%2+1), take, self.__sticks))
        
    def checkMove(self, take):
        """Prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht."""
        if self.__minTake > take or min(self.__maxTake, self.__sticks) < take:
            raise ValueError("wollte " + str(take) + " statt zwischen " + str(self.__minTake) + " und " + str(min(self.__maxTake, self.__sticks)) + " nehmen.")

    def __recordState(self, state):
        """Speichert den Zug und den Spielstand ab um am Ende des Spiels den Spielablauf sehen zu können."""
        self.__moveRecords.append(state)

    def getMoveRecords(self):
        """Gibt alle Züge zurück bzw. in kompakter Form aus."""
        s = ""
        for record in self.__moveRecords:
            if (record[1] >= 0):
                s += "(" + str(record[0]) + ") " + str(record[2]+record[3]) + " -" + str(record[2]) + " =>"
            else:
                s += " Spieler " + str(-record[1]) + " gewinnt nach " + str(record[0]) + " Zügen!"
        print (s)

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
    """Ein Callback für einen dummen Computerspieler."""
    nextTake = random.randint(game.minTake, game.maxTake)
    return (nextTake if nextTake < game.sticks else game.sticks)

def computer2(game):
    """Ein Callback für den optimalen Computerspieler."""
    nextTake = (game.sticks - 1) % (game.minTake + game.maxTake)
    return (nextTake if nextTake > 0 else 1)
