import random
import copy

# -------------------- class Kalaha --------------------
class Kalaha:
    def __init__(self, player1, player2):
        self.__numPits = 6
        stones = 4
        self.__pit = ([0] + [stones] * self.__numPits, [0] + [stones] * self.__numPits)
        self.__playerCallback = (player1, player2)
        self.__nextPlayer = 1
        self.__nextMove = 0
        self.__moveRecords = []

    @property
    def nextMove(self):
        return self.__nextMove

    @property
    def nextPlayer(self):
        return self.__nextPlayer

    @property
    def pit(self):
        return copy.deepcopy(self.__pit)

    def play(self):
        """Startet das Spiel und ruft alternierend beide Spieler-Strategien auf, bis eine gewinnt."""
        try:
            while self.__nextPlayer > 0:
                self.__nextMove += 1
                move = self.__playerCallback[self.__nextPlayer-1](self)
                self.checkMove(move)
                self.__doMove(move)
        except ValueError as e:
            self.__nextPlayer = -(self.__nextPlayer%2 + 1)
            self.__recordState((self.__nextMove, self.__nextPlayer, move, self.__pit))

    def checkMove(self, move):
        """Prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht."""
        if move < 1 or move > self.__numPits:
            raise ValueError("Gewählte Mulde " + str(move) + " ist ungültig!")
        if self.__pit[self.__nextPlayer-1][move] < 1:
            raise ValueError("In der gewählten Mulde " + str(move) + " gibt es keinen Steinen!")

    def __doMove(self, move):
        """Macht den aktuellen Zug und prüft ob der aktuelle Spieler gewonnen hat, oder sonst wird der nächste Zug vorbereitet."""
        # Zuerst entfernen wir alle Steine von der gewählten Mulde
        stones = self.__pit[self.__nextPlayer-1][move]
        self.__pit[self.__nextPlayer-1][move] = 0
        # Dann verteilen wir die Steine rekursiv auf die nächsten Mulden
        nextPlayer = self.__addStone(self.__nextPlayer-1, move-1, stones)
        self.__recordState((self.__nextMove, self.__nextPlayer, move, copy.deepcopy(self.__pit)))
        if self.__checkEnd():
            self.__nextPlayer = -self.__getWinner()
            self.__recordState((self.__nextMove, self.__nextPlayer, None, None))
            # TODO? self.printAllStates()
        else:
            self.__nextPlayer = nextPlayer

    def __addStone(self, row, pit, remaining):
        """Addiert 'remaining' Anzahl Steine angefangen von der gegebenen Mulde in der gegebenen Zeile, rekursiv."""
        if remaining < 1:
            # Nachdem alle Steine verteilt wurden, kommt der andere Spieler an der Reihe
            return self.__nextPlayer%2 + 1
        elif pit < 1:
            # In der eigener Reihe legen wir einen zusätzlichen Stein auch in den Kalah
            if row == self.__nextPlayer-1:
                self.__pit[row][0] += 1
                remaining -= 1
                # Wenn das der letzte Stein war, dann kommt nochmals dieser Spieler
                if remaining < 1:
                    return self.__nextPlayer
            # Sonst springen wir rüber auf die andere Reihe, zur letzten Mulde
            return self.__addStone((row + 1)%2, self.__numPits, remaining)
        else:
            # Wir legen einfach einen Stein ab in die aktuelle Mulde
            self.__pit[row][pit] += 1
            remaining -= 1
            if remaining < 1:
                stonesInOppositePit = self.__pit[(row+1)%2][self.__numPits+1-pit]
                # Wenn das der letzte Stein war und in eine eigene leere Mulde gestellt wurde,
                # deren gegenüberliegende Mulde nicht leer war, dann ...
                if row == self.__nextPlayer-1 and self.__pit[row][pit] == 1 and stonesInOppositePit > 0:
                    # ... speichern wir den Zwischenstand für bessere Nachvollziehbarkeit
                    # TODO? self.__recordState((self.__nextMove, self.__nextPlayer, "*", copy.deepcopy(self.__pit)))
                    # ... und verschieben alle Steine der beiden Mulden in den eigenen Kalah
                    self.__pit[row][0] += stonesInOppositePit + 1
                    self.__pit[row][pit] = 0
                    self.__pit[(row+1)%2][self.__numPits+1-pit] = 0
                # Nachdem alle Steine verteilt wurden, kommt der andere Spieler an der Reihe
                return self.__nextPlayer%2 + 1
            # Wenn das nicht der letzte Stein war, gehen wir weiter zur nächsten Mulde
            else:
                return self.__addStone(row, pit-1, remaining)

    def __checkEnd(self):
        """Gibt an ob das Spiel beendet ist (True) oder nicht (False)"""
        return sum(self.__pit[0][1:]) < 1 or sum(self.__pit[1][1:]) < 1

    def __getWinner(self):
        """Gibt an ob welcher Spieler (1 oder 2) das Spiel gewonnen hat"""
        stones1 = sum(self.__pit[0])
        stones2 = sum(self.__pit[1])
        return 1 if stones1 > stones2 else 2 if stones1 < stones2 else 0

    def __recordState(self, state):
        """Speichert den Zug und den Spielstand ab um am Ende des Spiels den Spielablauf sehen zu können."""
        self.__moveRecords.append(state)
        print(self.stateToString(state)) # TODO: Löschen!

    def stateToString(self, state):
        """Gibt ein einzelner Move-Rekord als String zurück."""
        s = ""
        if (state[1] > 0):
            s += gamePanelToString(state[3], "({:2d}/{:d}): {} => ".format(state[0], state[1], state[2]))
        else:
            s += "  Spieler {:d} gewinnt nach {:d} Zügen!".format(-state[1], state[0])
            if (state[2] != None):
                s += " Grund: Falscher Zug ({:d}) des anderen Spielers.".format(state[2])
        return s

    def printAllStates(self):
        """Gibt alle Züge zurück bzw. in kompakter Form aus."""
        s = ""
        for state in self.__moveRecords:
            print(self.stateToString(state))

# -------------------- Hilfsmethoden --------------------   
def gamePanelToString(gamePanel, firstLine = ""):
    pits1 = ["{:2d}".format(i) for i in gamePanel[0]]
    pits2 = ["{:2d}".format(i) for i in gamePanel[1][::-1]]
    return firstLine + " |".join(pits1) + " |   " + "\n" + " "*len(firstLine) + "   |" + " |".join(pits2)

# -------------------- Human player callback --------------------   
def human(game):
    """Ein Callback für einen menschlichen Spieler, der den Benutzer um ihren Zug fragt."""
    n = 0
    exc = ""
    while n == 0:
        try:
            n = int(input(exc + "Spieler " + str(game.nextPlayer) + ": " + str(game.nextMove) + ". Zug kommt, aus welcher Mulde"
                + " möchtest du die Steine schieben? "))
            game.checkMove(n)
        except ValueError as e:
            n = 0
            exc = str(e) + "! "
    return n

# -------------------- Computer player callbacks --------------------   
def computer1(game):
    """Ein Callback für einen dummen Computerspieler."""
    pitList = game.pit[game.nextPlayer-1]
    nonEmptyPitList = [i for i in range(len(pitList)) if i > 0 and pitList[i] > 0]
    return nonEmptyPitList[random.randint(0, len(nonEmptyPitList)-1)]

def computer2(game):
    """Ein Callback für einen halbwegs smarten Computerspieler."""
    pit = game.pit
    move = 0
    moveValue = -12
    for i in range(1, len(pit[game.nextPlayer-1])):
        stones = pit[game.nextPlayer-1][i]
        if stones == 0:
            continue
        # Zuerst schauen wir, ob es ein Zug gibt, der den letzten Stein gerade in Kalah bringt
        elif i == stones:
            return i
        # Sonst schauen wir, ob wir gegnerische Steine erbeuten können
        elif stones < i and pit[game.nextPlayer-1][i-stones] == 0 and pit[game.nextPlayer%2][7-i+stones] > 0:
            return i
        elif stones > i+6 and stones < 13 and pit[game.nextPlayer-1][i+13-stones] == 0:
            return i
        elif stones == 13:
            return i
        # Wir schauen auf die andere Seite ob die Mulde dort leer ist
        elif pit[game.nextPlayer%2][7-i] == 0 and stones > moveValue:
            move = i
            moveValue = stones
        # Sonst suchen wir den Zug, der die wenigsten Steine auf die andere Seite bringt
        elif i-stones > moveValue:
            move = i
            moveValue = i-stones
    # Den move-Zug geben wir aber nur dann zurück, wenn wir sonst keinen anderen guten Zug haben
    return move

# -------------------- MAIN --------------------   

game = Kalaha(computer2, human)
game.play()
#game.printAllStates()
