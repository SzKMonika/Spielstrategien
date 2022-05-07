"""Dieses Modul beinhaltet die Klasse VierGewinnt, eine konkrete Subklasse von Game."""

from games.game import Game
from functools import reduce
import copy, random, sys

# -------------------- class VierGewinnt --------------------
class VierGewinnt(Game):
    """Das ist ein konkretes Spiel (Game), das auf einem senkrecht stehenden aus sieben Spalten (senkrecht) und sechs Reihen (waagerecht) bestehenden
    hohlen Spielbrett gespielt wird. Jeder Spieler besitzt 21 gleichfarbige Spielsteine.
    Die Spieler lassen abwechselnd in einer der Spalten ihre Spielsteine fallen. Wenn ein Spieler einen Spielstein in eine Spalte fallen lässt,
    besetzt dieser den untersten freien Platz der Spalte. Gewinner ist der Spieler, der es als erster schafft, vier oder mehr seiner Spielsteine
    waagerecht, senkrecht oder diagonal in eine Linie nebeneinander zu bringen.
    Unten werden nur die VierGewinnt-spezifische Argumente und Attribute aufgeführt, für die sonstigen bitte im Game schauen.

    Attributes:
        __ROWS (int): Anzahl der Reihen auf dem Spielbrett (Konstante mit dem Wert 6).
        __COLUMNS (int): Anzahl der Spalten auf dem Spielbrett (Konstante mit dem Wert 7).
        __gamePanel: Eine zweidimensionale Liste von ganzen Zahlen, die jeweils den Wert 0 (leer), 1 (Spieler 1) oder -1 (Spieler 2) haben.
    """
    __ROWS = 6
    __COLUMNS = 7
    def __init__(self, player1, player2):
        super(VierGewinnt, self).__init__(player1, player2)
        self.__gamePanel = [[0]*self.__COLUMNS for _ in range(self.__ROWS)]

    @property
    def gamePanel(self):
        return copy.deepcopy(self.__gamePanel)    

    def checkMove(self, move):
        if not isinstance(move, int):
            raise ValueError("Es muss eine ganze Zahl angegeben werden!")
        if move < 1 or move > self.__COLUMNS:
            raise ValueError("Gewählte Spalte " + str(move) + " ist ungültig!")
        if VierGewinnt.countTokensIn(self.getColumn(move)) >= self.__ROWS:
            raise ValueError("Gewählte Spalte " + str(move) + " ist schon voll!")

    def _doMove(self, move):
        row = VierGewinnt.countTokensIn(self.getColumn(move)) + 1
        self.__gamePanel[row - 1][move - 1] = self.getTokenForNextPlayer()
        return (self.nextPlayer%2 + 1)

    def _checkEnd(self, move):
        row = VierGewinnt.countTokensIn(self.getColumn(move))
        winner = VierGewinnt.getWinnerIn(self.getColumn(move), self.getRow(row), self.getDiagonalUpRight(row, move), self.getDiagonalUpLeft(row, move))
        return winner if winner > 0 else 0 if self.countTokens() >= self.__ROWS*self.__COLUMNS else None

    def getTokenForNextPlayer(self):
        """Gibt den Wert des Tokens als ganze Zahl (1 oder -1) für nextPlayer zurück."""
        return 1 if self.nextPlayer == 1 else -1

    def countTokens(self):
        """Rechnet die Anzahl Spielsteine im Spielbrett zusammen, Reihe für Reihe."""
        count = 0
        for row in self.__gamePanel:
            count += sum([abs(token) for token in row])
        return count

    def getColumn(self, column):
        """Gibt den Inhalt der gewählten Spalte (1 bis 7) als eine Liste zurück."""
        return [row[column - 1] for row in self.__gamePanel]

    def getRow(self, row):
        """Gibt den Inhalt der gewählten Reihe (1 bis 6) als eine Liste zurück."""
        return list(self.__gamePanel[row - 1])

    def getDiagonalUpRight(self, row, column):
        """Gibt den Inhalt der diagonalen Linie (von unten links nach oben rechts) zurück, die durch das angegebene Feld durchläuft."""
        placesDownLeft = min(row - 1, column - 1)
        placesUpRight = min(self.__ROWS - row, self.__COLUMNS - column)
        line = []
        for i in range(placesDownLeft + placesUpRight + 1):
            line.append(self.__gamePanel[row - 1 - placesDownLeft + i][column - 1 - placesDownLeft + i])
        return line
        
    def getDiagonalUpLeft(self, row, column):
        """Gibt den Inhalt der diagonalen Linie (von unten rechts nach oben links) zurück, die durch das angegebene Feld durchläuft."""
        placesDownRight = min(row - 1, self.__COLUMNS - column)
        placesUpLeft = min(self.__ROWS - row, column - 1)
        line = []
        for i in range(placesDownRight + placesUpLeft + 1):
            line.append(self.__gamePanel[row - 1 - placesDownRight + i][column - 1 + placesDownRight - i])
        return line

    def gamePanelToString(self, gamePanel, firstLine = ""):
        s = ""
        for row in gamePanel[::-1]:
            if VierGewinnt.countTokensIn(row) >= 0:
                s += ("\n" + " "*len(firstLine) if len(s) > 0 else "") + reduce(lambda s, e: s + VierGewinnt.tokenToString(e), row, "")
        return firstLine + s + "\n"

    # -------------------- Hilfsmethoden --------------------   
    @staticmethod
    def getWinnerIn(*lines):
        """Gibt zurück, ob es in der angegebenen Liste von Linien eine gibt, in der mind. 4 gleiche benachbarte Spielsteine vorkommen."""
        for line in lines:
            countSame = VierGewinnt.countSameTokensIn(line)
            if abs(countSame) > 3:
                return 1 if countSame > 0 else 2
        return 0

    @staticmethod
    def countSameTokensIn(line):
        """Gibt an, wie viele gleiche Tokens benachbart in einer Reihe von Zahlen vorkommen."""
        sum = maxSum = minSum = 0
        for token in line:
            sum = sum + token if token*sum > 0 else token
            maxSum = sum if sum > maxSum else maxSum
            minSum = sum if sum < minSum else minSum
        return minSum if -minSum > maxSum else maxSum

    @staticmethod
    def countTokensIn(line):
        """Gibt an, wie viele Spielsteine insgesamt in der angegebenen Linie vorkommen."""
        return sum([abs(token) for token in line])

    @staticmethod
    def tokenToString(token):
        """Gibt die menschliche Repräsentation (X, O oder .) eines Spielfeldes zurück."""
        return "X " if token == 1 else "O " if token == -1 else ". " if token == 0 else "? "

    # -------------------- Computer Strategien --------------------   
    @staticmethod
    def level1(game):
        """Strategie für einen dummen Computerspieler."""
        maxRow = 6
        maxCol = 7    
        nonFullColList = [i for i in range(1, maxCol + 1) if VierGewinnt.countTokensIn(game.getColumn(i)) < maxRow]
        return nonFullColList[random.randint(0, len(nonFullColList) - 1)]

    @staticmethod
    def level2(game):
        """Strategie für einen einfachen Computerspieler."""
        maxRow = 6
        maxCol = 7

        for col in range(1, maxCol + 1):
            row = VierGewinnt.countTokensIn(game.getColumn(col)) + 1
            if row > maxRow:
                pass
            # Zuerst prüfen wir ob wir hier gewinnen könnten
            elif VierGewinnt.hasWinnerWithTokenIn(game, row, col, game.getTokenForNextPlayer()):
                return col
            # Dann prüfen wir ob der Gegner hier gewinnen könnte
            elif VierGewinnt.hasWinnerWithTokenIn(game, row, col, -game.getTokenForNextPlayer()):
                return col
        return VierGewinnt.level1(game)

    @staticmethod
    def level3(game):
        """Strategie für einen mittelmässigen Computerspieler."""
        maxRow = 6
        maxCol = 7
        # Wenn wir keinen besseren Zug finden werden, dann wählen wir die mittlere Spalte ausser
        # wenn es voll ist. Im letzteren Fall rufen wir die Strategie level1() auf.
        move = (maxCol + 1)//2 if VierGewinnt.countTokensIn(game.getColumn((maxCol + 1)//2)) < maxRow else VierGewinnt.level1(game)

        for col in range(1, maxCol + 1):
            row = VierGewinnt.countTokensIn(game.getColumn(col)) + 1
            if row > maxRow:
                pass
            # Zuerst prüfen wir ob wir hier gewinnen könnten
            elif VierGewinnt.hasWinnerWithTokenIn(game, row, col, game.getTokenForNextPlayer()):
                return col
            # Dann prüfen wir ob der Gegner hier gewinnen könnte
            elif VierGewinnt.hasWinnerWithTokenIn(game, row, col, -game.getTokenForNextPlayer()):
                move = col
        return move

    @staticmethod
    def level4(game):
        """Strategie für einen smarten Computerspieler."""
        maxRow = 6
        maxCol = 7
        move = 0
        moveValue = 0
        for col in range(1, maxCol + 1):
            row = VierGewinnt.countTokensIn(game.getColumn(col)) + 1
            if row > maxRow:
                pass
            # Zuerst prüfen wir ob wir hier gewinnen könnten
            elif VierGewinnt.hasWinnerWithTokenIn(game, row, col, game.getTokenForNextPlayer()):
                return col
            # Dann prüfen wir ob der Gegner hier gewinnen könnte
            elif VierGewinnt.hasWinnerWithTokenIn(game, row, col, -game.getTokenForNextPlayer()):
                move = col
                moveValue = sys.maxsize
            # Ansonsten merken wir die Stelle mit dem grössten Wert...
            elif moveValue < VierGewinnt.getPlaceValue(row, col, maxRow, maxCol):
                # ...und prüfen, dass der Gegner im nächsten Zug in der gleichen Spalte nicht gewinnnen kann
                if not(row < maxRow and VierGewinnt.hasWinnerWithTokenIn(game, row + 1, col, -game.getTokenForNextPlayer())):
                    move = col
                    moveValue = VierGewinnt.getPlaceValue(row, col, maxRow, maxCol)
        return move

    @staticmethod
    def hasWinnerWithTokenIn(game, row, col, token, maxCol = 7):
        """Diese Methode rechnet basierend auf dem Spielbrett vom 'game' aus, ob jemand gewinnen würde wenn auf die gegebene Position (row, col)
        noch ein 'token' gestellt wäre.
        """
        lineCol = game.getColumn(col)
        lineRow = game.getRow(row)
        lineDiag1 = game.getDiagonalUpRight(row, col)
        lineDiag2 = game.getDiagonalUpLeft(row, col)
        lineCol[row - 1] = token
        lineRow[col - 1] = token
        lineDiag1[min(row, col) - 1] = token
        lineDiag2[min(row, maxCol + 1 - col) - 1] = token
        win = VierGewinnt.getWinnerIn(lineCol, lineRow, lineDiag1, lineDiag2) > 0
        # In der ersten Zeile würde eine beidseitig offene "3-er Reihe" auch (im nächsten Zug) schon gewinnen
        if row == 1 and VierGewinnt.countSameTokensIn(lineRow) == 3:
            sameCountList = VierGewinnt.getSameCountList(lineRow, 0.4)
            # Falls es eine beidseitig offene 3-er Reihe vorhanden ist, dann muss der absolutWert von minimum oder maximum genau 3,8 sein.
            if token < 0 and min(sameCountList) < -3.5 or token > 0 and max(sameCountList) > 3.5:
                win = True
        return win

    @staticmethod
    def getSameCountList(line, extraForEmptyNeigbour = 0.4):
        """Verarbeitet eine Liste von Zahlen so, dass benachbarte Zahlen mit gleichen Vorzeichen in einer Zahl zusammenaddiert werden und wenn die Zahlenketten
        mit einer leeren Stelle (0) benachbart sind, dann gibt es für jede dieser leere Nachbarstellen eine extra Punktezahl dazuaddiert.
        """
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

    @staticmethod
    def getPlaceValue(row, col, maxRow = 6, maxCol = 7):
        """Kalkuliert den Wert einer Stelle, also die Anzahl 4-er Ketten die über dieser Stelle laufen."""
        downLeft = min(row, col)
        upRight = min(maxRow + 1 - row, maxCol + 1 - col)
        downRight = min(row, maxCol + 1 - col)
        upLeft = min(maxRow + 1 - row, col)
        diagonal1 = min(downLeft, upRight, max(downLeft + upRight - 4, 0))
        diagonal2 = min(downRight, upLeft, max(downRight + upLeft - 4, 0))
        return min(row, maxRow + 1 - row) + min(col, maxCol + 1 - col) + diagonal1 + diagonal2
