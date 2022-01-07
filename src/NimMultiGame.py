import random

# -------------------- class NimMultiGame --------------------
class NimMultiGame:
    def __init__(self, player1, player2, sticksList, lastOneLoses = False):
        self.__sticksList = sticksList
        self.__lastOneLoses = lastOneLoses
        self.__player = (player1, player2)
        self.__nextPlayer = 1
        self.__nextMove = 0
        self.__moveRecords = []

    @property
    def sticksList(self):
        return list(self.__sticksList)    

    @property
    def lastOneLoses(self):
        return self.__lastOneLoses

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
            self.__nextPlayer = -self.__nextPlayer if self.__lastOneLoses else -(self.__nextPlayer%2+1)
            self.__recordState((self.__nextMove, self.__nextPlayer, None, None))
        except ValueError as e:
            self.__recordState((self.__nextMove, -(self.__nextPlayer%2+1), take, self.__sticksList))
        
    def checkMove(self, take):
        """Prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht."""
        if take[0] < 1 or take[0] > len(self.__sticksList) or take[1] < 1 or take[1] > self.__sticksList[take[0]-1]:
            raise ValueError("Unmöglicher Zug: " + str(take))

    def __recordState(self, state):
        """Speichert den Zug und den Spielstand ab um am Ende des Spiels den Spielablauf sehen zu können."""
        self.__moveRecords.append(state)

    def stateToString(self, state):
        """Gibt den Spielstand nach einem Zug in kompakter/ausdruckbarer Form zurück."""
        s = ""
        if (state[1] >= 0):
            s += "({:2d}/{:d}): {} => {}".format(state[0], state[1], state[2], state[3])
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
    n = None
    exc = ""
    while n is None:
        try:
            n = str(input(exc + str(game.nextMove) + ". Zug kommt und es sind noch " + str(game.sticksList) + " Sticks da. Wie viel nimmst du weg? "))
            game.checkMove(eval(n))
        except ValueError as e:
            n = None
            exc = str(e) + "! "
    return eval(n)

# -------------------- Computer player callbacks --------------------   
def computer1(game):
    """Callback für einen dummen Computerspieler."""
    sticksList = game.sticksList
    nonEmptySticksList = [(i, sticksList[i]) for i in range(len(sticksList)) if sticksList[i] > 0]
    row = random.randint(0, len(nonEmptySticksList)-1)
    take = random.randint(1, nonEmptySticksList[row][1])
    return (nonEmptySticksList[row][0] + 1, take)

def computer2(game):
    """Callback für einen mittelmässigen Computerspieler."""
    sticksList = game.sticksList
    maxSticks = 0
    maxIndex = 0
    countRowOne = 0
    countRowMore = 0
    # Wir zählen die Anzahl Reihen mit einem bzw. mehr Sticks...
    for i in range(len(sticksList)):
        #...und wir merken auch die Reihe mit den meisten Sticks.
        if sticksList[i] > maxSticks:
            maxIndex = i
            maxSticks = sticksList[i]
        if sticksList[i] > 1:
            countRowMore += 1
        elif sticksList[i] == 1:
            countRowOne += 1
    # Wenn es nur Reihen mit einem Stick gibt, dann müssen/können wir eine beliebige nehmen
    if countRowMore == 0:
        return (maxIndex + 1, 1)
    # Wenn es nur noch eine Reihe mit mehr als einem Stick gibt oder mehr als 3 UND auch mind. 1-er Reihe...
    elif countRowMore == 1 or (countRowMore > 2 and countRowOne > 0):
        #...dann nehmen wir alle oder alle bis auf einem Stick weg, so dass gerade passende Anzahl an 1-er Reihen bleiben.
        return (maxIndex + 1, maxSticks if bool(countRowOne % 2 == 0) ^ bool(game.lastOneLoses) else maxSticks-1)
    # Sonst lassen wir 2 stehen oder wenn es nur 2 gibt, dann nehmen wir beide weg
    else:
        return (maxIndex + 1, maxSticks-2 if maxSticks > 2 else 2)

#-------------MAIN
nimGame = NimMultiGame(human, computer2, [1,3,5,7])
nimGame.play()
nimGame.printAllStates()
