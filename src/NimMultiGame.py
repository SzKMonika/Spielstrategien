import random

# -------------------- class NimMultiGame --------------------
class NimMultiGame:
    def __init__(self, player1, player2, sticksList):
        self.__sticksList = sticksList
        self.__player = (player1, player2)
        self.__nextPlayer = 1
        self.__nextMove = 0
        self.__moveRecords = []

    @property
    def sticksList(self):
        return list(self.__sticksList)    

    @property
    def nextMove(self):
        return self.__nextMove

    def isNotFinished(self):
        return sum(self.__sticksList) > 0

    def play(self):
        """Startet das Spiel und ruft alternierend beide Spieler-Strategien auf, bis eine gewinnt."""
        try:
            while self.isNotFinished():
                self.__nextMove += 1
                take = self.__player[self.__nextPlayer-1](self)
                self.checkMove(take)
                self.__sticksList[take[0]-1] = self.__sticksList[take[0]-1] - take[1]
                self.__recordState((self.__nextMove, self.__nextPlayer, take, list(self.__sticksList)))
                self.__nextPlayer = (self.__nextPlayer%2+1)
            self.__recordState((self.__nextMove, -self.__nextPlayer, None, None))
        except ValueError as e:
            self.__recordState((self.__nextMove, -(self.__nextPlayer%2+1), take, self.__sticksList))
        
    def checkMove(self, take):
        """Prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht."""
        if take[0] < 1 or take[0] > len(self.__sticksList) or take[1] < 1 or take[1] > self.__sticksList[take[0]-1]:
            raise ValueError("Unmöglicher Zug: " + str(take))

    def __recordState(self, state):
        """Speichert den Zug und den Spielstand ab um am Ende des Spiels den Spielablauf sehen zu können."""
        self.__moveRecords.append(state)

    def getMoveRecords(self):
        """Gibt alle Züge zurück bzw. in kompakter Form aus."""
        s = ""
        for record in self.__moveRecords:
            if (record[1] >= 0):
                s += "(" + str(record[0]) + "/" + str(record[1]) + ") " + str(record[2]) + " => " + str(record[3]) + "\n"
            else:
                s += " Spieler " + str(-record[1]) + " gewinnt nach " + str(record[0]) + " Zügen!"
        print (s)

# -------------------- Human player callback --------------------   
def human(game):
    """Ein Callback für einen menschlichen Spieler, der den Benutzer um ihren Zug fragt."""
    n = str(input(str(game.nextMove) + ". Zug kommt und es sind noch " + str(game.sticksList) + " Sticks da. Wie viel nimmst du weg?\n"
        + "..."))
    return eval(n)

# -------------------- Computer player callbacks --------------------   
def computer1(game):
    """Callback für einen dummen Computerspieler."""
    lst = game.sticksList
    nonEmptySticksList = [(i, lst[i]) for i in range(len(lst)) if lst[i] > 0]
    row = random.randint(0, len(nonEmptySticksList)-1)
    take = random.randint(1, nonEmptySticksList[row][1])
    return (nonEmptySticksList[row][0] + 1, take)

#-------------MAIN
nimGame = NimMultiGame(computer1, computer1, [1,3,5,7])
nimGame.play()
nimGame.getMoveRecords()
