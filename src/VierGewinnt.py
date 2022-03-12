from Game import Game, human
import copy
from functools import reduce
import random

# -------------------- class VierGewinnt --------------------
class VierGewinnt(Game):
    __ROWS = 6
    __COLUMNS = 7
    def __init__(self, player1, player2):
        super(VierGewinnt, self).__init__(player1, player2)
        self.__gamePanel = [[0]*self.__COLUMNS for _ in range(self.__ROWS)]

    @property
    def gamePanel(self):
        return copy.deepcopy(self.__gamePanel)    

    def checkMove(self, move):
        """Prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht."""
        if not isinstance(move, int):
            raise ValueError("Es muss eine ganze Zahl angegeben werden!")
        if move < 1 or move > self.__COLUMNS:
            raise ValueError("Gewählte Spalte " + str(move) + " ist ungültig!")
        if countTokensIn(self.getColumn(move)) >= self.__ROWS:
            raise ValueError("Gewählte Spalte " + str(move) + " ist schon voll!")

    def _doMove(self, move):
        """Macht den aktuellen Zug und gibt zurück welcher Spieler als nächster kommt."""
        row = countTokensIn(self.getColumn(move)) + 1
        self.__gamePanel[row - 1][move - 1] = self.getTokenForNextPlayer()
        return (self.nextPlayer%2 + 1)

    def _checkEnd(self, move):
        """Gibt an ob das Spiel mit unentschieden beendet ist (0) oder ein Spieler gewonnen hat (1 oder 2), oder noch nicht beendet ist (None)"""
        row = countTokensIn(self.getColumn(move))
        winner = getWinnerIn(self.getColumn(move), self.getRow(row), self.getDiagonalUpRight(row, move), self.getDiagonalUpLeft(row, move))
        return winner if winner > 0 else 0 if self.countTokens() >= self.__ROWS*self.__COLUMNS else None

    def getTokenForNextPlayer(self):
        return 1 if self.nextPlayer == 1 else -1

    def countTokens(self):
        count = 0
        for row in self.__gamePanel:
            count += sum([abs(token) for token in row])
        return count

    def getColumn(self, column):
        return [row[column - 1] for row in self.__gamePanel]

    def getRow(self, row):
        return list(self.__gamePanel[row - 1])

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

    def gamePanelToString(self, gamePanel, firstLine = ""):
        s = ""
        for row in gamePanel[::-1]:
            if countTokensIn(row) >= 0:
                s += ("\n" + " "*len(firstLine) if len(s) > 0 else "") + reduce(lambda s, e: s + tokenToString(e), row, "")
        return firstLine + s + "\n"

# -------------------- Utility methods --------------------   
def getWinnerIn(*lines):
    for line in lines:
        countSame = countSameTokensIn(line)
        if abs(countSame) > 3:
            return 1 if countSame > 0 else 2
    return 0

def countSameTokensIn(line):
    """Gibt an wie viele gleiche Tokens benachbart in einer Reihe von Zahlen vorkommen."""
    sum = maxSum = minSum = 0
    for token in line:
        sum = sum + token if token*sum > 0 else token
        maxSum = sum if sum > maxSum else maxSum
        minSum = sum if sum < minSum else minSum
    return minSum if -minSum > maxSum else maxSum

def countTokensIn(line):
    return sum([abs(token) for token in line])

def tokenToString(token):
    return "X " if token == 1 else "O " if token == -1 else ". " if token == 0 else "? "

# -------------------- Computer Strategien --------------------   
def VierGewinnt_L1(game):
    """Strategie für einen dummen Computerspieler."""
    maxRow = 6
    maxCol = 7    
    nonFullColList = [i for i in range(1, maxCol + 1) if countTokensIn(game.getColumn(i)) < maxRow]
    return nonFullColList[random.randint(0, len(nonFullColList) - 1)]

def VierGewinnt_L2(game):
    """Strategie für einen einfachen Computerspieler."""
    maxRow = 6
    maxCol = 7

    for col in range(1, maxCol + 1):
        row = countTokensIn(game.getColumn(col)) + 1
        if row > maxRow:
            pass
        # Zuerst prüfen wir ob wir hier gewinnen könnten
        elif hasWinnerWithTokenIn(game, row, col, game.getTokenForNextPlayer()):
            return col
        # Dann prüfen wir ob der Gegner hier gewinnen könnte
        elif hasWinnerWithTokenIn(game, row, col, -game.getTokenForNextPlayer()):
            return col
    return VierGewinnt_L1(game)

def VierGewinnt_L3(game):
    """Strategie für einen einfachen Computerspieler."""
    maxRow = 6
    maxCol = 7

    for col in range(1, maxCol + 1):
        row = countTokensIn(game.getColumn(col)) + 1
        if row > maxRow:
            pass
        # Zuerst prüfen wir ob wir hier gewinnen könnten
        elif hasWinnerWithTokenIn(game, row, col, game.getTokenForNextPlayer()):
            return col
        # Dann prüfen wir ob der Gegner hier gewinnen könnte
        elif hasWinnerWithTokenIn(game, row, col, -game.getTokenForNextPlayer()):
            return col
    return (maxCol + 1)//2 if countTokensIn(game.getColumn((maxCol + 1)//2)) < maxRow else VierGewinnt_L1(game)

def VierGewinnt_L4(game):
    """Strategie für einen smarten Computerspieler."""
    maxRow = 6
    maxCol = 7
    selectedCol = 0
    selectedValue = 0
    for col in range(1, maxCol + 1):
        row = countTokensIn(game.getColumn(col)) + 1
        if row > maxRow:
            pass
        # Zuerst prüfen wir ob wir hier gewinnen könnten
        elif hasWinnerWithTokenIn(game, row, col, game.getTokenForNextPlayer()):
            return col
        # Dann prüfen wir ob der Gegner hier gewinnen könnte
        elif hasWinnerWithTokenIn(game, row, col, -game.getTokenForNextPlayer()):
            selectedCol = col
            selectedValue = 1000
        # Ansonsten merken wir die Stelle mit dem grössten Wert...
        elif selectedValue < getPlaceValue(row, col, maxRow, maxCol):
            # ...und prüfen, dass der Gegner im nächsten Zug in der gleichen Spalte nicht gewinnnen kann
            if not(row < maxRow and hasWinnerWithTokenIn(game, row + 1, col, -game.getTokenForNextPlayer())):
                selectedCol = col
                selectedValue = getPlaceValue(row, col, maxRow, maxCol)
    return selectedCol

def hasWinnerWithTokenIn(game, row, col, token, maxCol = 7):
    lineCol = game.getColumn(col)
    lineRow = game.getRow(row)
    lineDiag1 = game.getDiagonalUpRight(row, col)
    lineDiag2 = game.getDiagonalUpLeft(row, col)
    lineCol[row - 1] = token
    lineRow[col - 1] = token
    lineDiag1[min(row, col) - 1] = token
    lineDiag2[min(row, maxCol + 1 - col) - 1] = token
    win = getWinnerIn(lineCol, lineRow, lineDiag1, lineDiag2) > 0
    # In der ersten Zeile würde eine beidseitig offener "3-er Reihe" auch (im nächsten Zug) schon gewinnen
    if row == 1 and countSameTokensIn(lineRow) == 3:
        sameCountList = getSameCountList(lineRow, 0.4)
        if token < 0 and min(sameCountList) < -3.5 or token > 0 and max(sameCountList) > 3.5:
            win = True
    return win

def getSameCountList(line, extraForEmptyNeigbour = 0.4):
    sameCountList = [line[0]]
    for i in range(1, len(line)):
        if sameCountList[-1]*line[i] > 0:
            sameCountList[-1] += line[i]
        elif sameCountList[-1]*line[i] < 0:
            sameCountList.append(line[i])
        elif sameCountList[-1] != 0 and line[i] == 0:
            sameCountList[-1] += extraForEmptyNeigbour if sameCountList[-1] > 0 else -extraForEmptyNeigbour
            sameCountList.append(line[i])
        elif sameCountList[-1] == 0 and line[i] != 0:
            sameCountList.append(line[i]*(1 + extraForEmptyNeigbour))
    return sameCountList

def getPlaceValue(row, col, maxRow = 6, maxCol = 7):
    """Kalkuliert den Wert einer Stelle, also die Anzahl 4-er Ketten die über dieser Stelle laufen."""
    downLeft = min(row, col)
    upRight = min(maxRow + 1 - row, maxCol + 1 - col)
    downRight = min(row, maxCol + 1 - col)
    upLeft = min(maxRow + 1 - row, col)
    diagonal1 = min(downLeft, upRight, max(downLeft + upRight - 4, 0))
    diagonal2 = min(downRight, upLeft, max(downRight + upLeft - 4, 0))
    return min(row, maxRow + 1 - row) + min(col, maxCol + 1 - col) + diagonal1 + diagonal2
