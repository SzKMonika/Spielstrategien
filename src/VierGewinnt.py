import copy
from functools import reduce
import random

# -------------------- class VierGewinnt --------------------
class VierGewinnt:
    __ROWS = 6
    __COLUMNS = 7
    def __init__(self, player1, player2):
        self.__gamePanel = [[0]*self.__COLUMNS for _ in range(self.__ROWS)]
        self.__playerCallback = (player1, player2)
        self.__nextPlayer = 1
        self.__nextMove = 0
        self.__moveRecords = []

    @property
    def gamePanel(self):
        return copy.deepcopy(self.__gamePanel)    

    @property
    def nextMove(self):
        return self.__nextMove

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
            self.__recordState((self.__nextMove, self.__nextPlayer, move, self.__gamePanel))

    def checkMove(self, move):
        """Prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht."""
        if move < 1 or move > self.__COLUMNS:
            raise ValueError("Gewählte Spalte " + str(move) + " ist ungültig!")
        if countTokensIn(self.getColumn(move)) >= self.__ROWS:
            raise ValueError("Gewählte Spalte " + str(move) + " ist schon voll!")

    def __doMove(self, column):
        """Macht den aktuellen Zug und prüft ob der aktuelle Spieler gewonnen hat, oder sonst wird der nächste Zug vorbereitet."""
        row = countTokensIn(self.getColumn(column)) + 1
        self.__gamePanel[row-1][column-1] = self.getTokenForNextPlayer()
        self.__recordState((self.__nextMove, self.__nextPlayer, column, copy.deepcopy(self.__gamePanel)))
        # TODO: Es kann auch unentschieden werden, wenn alle Felder gefüllt sind!
        if self.__checkEnd(row, column):
            self.__nextPlayer = -self.__nextPlayer
            self.__recordState((self.__nextMove, self.__nextPlayer, None, None))
        else:
            self.__nextPlayer = (self.__nextPlayer % 2 + 1)

    def __checkEnd(self, row, column):
        """Gibt an ob das Spiel beendet ist (True) oder nicht (False)"""
        if hasWinnerIn(self.getColumn(column), self.getRow(row), self.getDiagonalUpRight(row, column), self.getDiagonalUpLeft(row, column)):
            return True
        return self.countTokens() >= self.__ROWS * self.__COLUMNS

    def getTokenForNextPlayer(self):
        return 1 if self.__nextPlayer == 1 else -1

    def countTokens(self):
        count = 0
        for row in self.__gamePanel:
            count += sum([abs(token) for token in row])
        return count

    def getColumn(self, column):
        return [row[column-1] for row in self.__gamePanel]

    def getRow(self, row):
        return list(self.__gamePanel[row-1])

    def getDiagonalUpRight(self, row, column):
        placesDownLeft = min(row - 1, column - 1)
        placesUpRight = min(self.__ROWS - row, self.__COLUMNS - column)
        line = []
        for i in range(placesDownLeft + placesUpRight + 1):
            line.append(self.__gamePanel[row - 1 - placesDownLeft + i][column - 1 - placesDownLeft + i])
        return line
        
    def getDiagonalUpLeft(self, row, column):
        placesDownRight = min(row - 1, self.__COLUMNS - column)
        placesUpLeft = min(self.__ROWS - row, column - 1)
        line = []
        for i in range(placesDownRight + placesUpLeft + 1):
            line.append(self.__gamePanel[row - 1 - placesDownRight + i][column - 1 + placesDownRight - i])
        return line

    def __recordState(self, state):
        """Speichert den Zug und den Spielstand ab um am Ende des Spiels den Spielablauf sehen zu können."""
        self.__moveRecords.append(state)
        print(self.stateToString(state)) # TODO: Remove later

    def stateToString(self, state):
        """Gibt den Spielstand nach einem Zug in kompakter/ausdruckbarer Form zurück."""
        s = ""
        if (state[1] >= 0):
            s += gamePanelToString(state[3], "({:2d}/{:d}): {} => ".format(state[0], state[1], state[2]))
        else:
            s += "  Spieler {:d} gewinnt nach {:d} Zügen!".format(-state[1], state[0])
            if (state[2] != None):
                s += " Grund: Falscher Zug ({:d}) des anderen Spielers.".format(state[2])
        return s

    def printAllStates(self):
        """Gibt alle Züge zurück bzw. in kompakter Form aus."""
        for state in self.__moveRecords:
            print(self.stateToString(state))

# -------------------- Utility methods --------------------   
def hasWinnerIn(*lines):
    for line in lines:
        if abs(countSameTokensIn(line)) > 3:
            return True
    return False

def countSameTokensIn(line):
    """Gibt an wie viele gleiche Tokens benachbart in einer Reihe von Zahlen vorkommen."""
    sum = maxSum = minSum = 0
    for token in line:
        sum = sum + token if token * sum > 0 else token
        maxSum = sum if sum > maxSum else maxSum
        minSum = sum if sum < minSum else minSum
    return minSum if -minSum > maxSum else maxSum

def countTokensIn(line):
    return sum([abs(token) for token in line])

def tokenToString(token):
    return "X " if token == 1 else "O " if token == -1 else "  " if token == 0 else "? "

def gamePanelToString(gamePanel, firstLine = ""):
    s = ""
    for row in gamePanel[::-1]:
        if countTokensIn(row) > 0:
            s += ("\n" + " "*len(firstLine) if len(s) > 0 else "") + reduce(lambda s, e: s + tokenToString(e), row, "")
    return firstLine + s

# -------------------- Human player callback --------------------   
def human(game):
    """Ein Callback für einen menschlichen Spieler, der den Benutzer um ihren Zug fragt."""
    n = 0
    exc = ""
    while n == 0:
        try:
            n = int(input(exc + str(game.nextMove) + ". Zug kommt, in welcher Spalte möchtest du dein Token werfen? "))
            game.checkMove(n)
        except ValueError as e:
            n = 0
            exc = str(e) + "! "
    return n

# -------------------- Computer player callbacks --------------------   
def computer1(game):
    """Ein Callback für einen dummen Computerspieler."""
    return random.randint(1, 7)

def computer2(game):
    """Ein Callback für einen smarten Computerspieler."""
    maxRow = 6
    maxCol = 7
    selectedCol = 0
    selectedValue = 0
    for col in range(1, 7):
        row = countTokensIn(game.getColumn(col)) + 1
        if row > maxRow:
            continue
        # Zuerst prüfen wir ob wir hier gewinnen könnten
        elif hasWinnerWithTokenIn(row, col, game.getTokenForNextPlayer()):
            return col
        # Dann prüfen wir ob der Gegner hier gewinnen könnte
        elif hasWinnerWithTokenIn(row, col, -game.getTokenForNextPlayer()):
            selectedCol = col
            selectedValue = 1000
        # TODO: Prüfen ob in der ersten Zeile eine beidseitig offener "2-er Reihe" schon gibt, und wenn ja, schliessen
        # Ansonsten merken wir die Stelle mit dem grössten Wert...
        elif selectedValue < getPlaceValue(row, col, maxRow, maxCol):
            # ...und prüfen, dass der Gegner im nächsten Zug in der gleichen Spalte nicht gewinnnen kann
            if not(row < maxRow and hasWinnerWithTokenIn(row+1, col, -game.getTokenForNextPlayer())):
                selectedCol = col
                selectedValue = getPlaceValue(row, col, maxRow, maxCol)
    return selectedCol

def hasWinnerWithTokenIn(row, col, token, maxCol = 7):
    lineCol = game.getColumn(col)
    lineRow = game.getRow(row)
    lineDiag1 = game.getDiagonalUpRight(row, col)
    lineDiag2 = game.getDiagonalUpLeft(row, col)
    lineCol[row-1] = token
    lineRow[col-1] = token
    lineDiag1[min(row, col)-1] = token
    lineDiag2[min(row, maxCol+1-col)-1] = token
    return hasWinnerIn(lineCol, lineRow, lineDiag1, lineDiag2)

def getPlaceValue(row, col, maxRow = 6, maxCol = 7):
    """Kalkuliert den Wert einer Stelle, also die Anzahl 4-er Ketten die über dieser Stelle laufen."""
    downLeft = min(row, col)
    upRight = min(maxRow+1-row, maxCol+1-col)
    downRight = min(row, maxCol+1-col)
    upLeft = min(maxRow+1-row, col)
    diagonal1 = min(downLeft, upRight, max(downLeft+upRight-4, 0))
    diagonal2 = min(downRight, upLeft, max(downRight+upLeft-4, 0))
    return min(row, maxRow+1-row) + min(col, maxCol+1-col) + diagonal1 + diagonal2

#-------------MAIN
game = VierGewinnt(human, computer2)
game.play()
#game.printAllStates()
