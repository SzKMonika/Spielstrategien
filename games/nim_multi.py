"""Dieses Modul beinhaltet die Klasse NimMulti, eine konkrete Subklasse von Game."""

from games.game import Game
from functools import reduce
import random

# -------------------- class NimMulti --------------------
class NimMulti(Game):
    """Das ist ein konkretes Spiel (Game), wo die zwei Spieler abwechselnd beliebige Anzahl an Objekten aus einer beliebigen Reihe wegnehmen, aus einer
    am Anfang des Spiels vordefinierten Anzahl an Objekten die in Reihen eingeteilt sind (sticksList).
    Gewonnen hat beim Standardspiel (lastOneLoses=False) derjenige, der das letzte Stück nimmt, bei der Misère-Variante (lastOneLoses=True) verliert dieser.
    Unten werden nur die Nim-spezifische Argumente und Attribute aufgeführt, für die sonstigen bitte im Game schauen.

    Args:
        sticksList: Eine Liste mit positiven ganzen Zahlen, die die Anzahl der Objekte in der jeweiligen Reihe beim Spielbeginn angeben.
        lastOneLoses (bool): Gibt an, welche Variante gespielt wird. False bedeutet die Standard-Variante, True bedeutet die Misère-Variante.

    Attributes:
        __sticksList: Eine Liste mit den aktuellen Anzahl der Objekten in den jeweiligen Reihen, am Anfang 'sticksList'.
        __lastOneLoses (bool): Die Spielvariante, die als 'lastOneLoses' angegeben wurde.
    """
    def __init__(self, player1, player2, sticksList = [1, 3, 5, 7], lastOneLoses = False):
        super(NimMulti, self).__init__(player1, player2)
        self.__sticksList = sticksList
        self.__lastOneLoses = lastOneLoses

    @property
    def gamePanel(self):
        return list(self.__sticksList)    

    @property
    def lastOneLoses(self):
        """Gibt an, welche Variante gespielt wird. False bedeutet die Standard-Variante, True bedeutet die Misère-Variante."""
        return self.__lastOneLoses

    def checkMove(self, move):
        if not isinstance(move, tuple):
            raise ValueError("Es müssen zwei mit Komma getrennten ganze Zahlen angegeben werden!")
        if move[0] < 1 or move[0] > len(self.__sticksList):
            raise ValueError("Gewählte Reihe " + str(move[0]) + " ist ungültig!")
        if move[1] < 1 or move[1] > self.__sticksList[move[0] - 1]:
            raise ValueError("In der gewählten Reihe " + str(move[0]) + " wollte man eine ungültige Anzahl " + str(move[1]) + " wegnehmen!")

    def _doMove(self, move):
        self.__sticksList[move[0] - 1] = self.__sticksList[move[0] - 1] - move[1]
        return (self.nextPlayer%2 + 1)

    def _checkEnd(self, move):
        return None if sum(self.__sticksList) > 0 else (self.nextPlayer%2 + 1) if self.__lastOneLoses else self.nextPlayer

    def getName(self):
        return type(self).__name__ + (" Misere" if self.__lastOneLoses else "")

    # -------------------- Computer Strategien --------------------   
    @staticmethod
    def level1(game):
        """Strategie für einen dummen Computerspieler."""
        sticksList = game.gamePanel
        nonEmptySticksList = [(i, sticksList[i]) for i in range(len(sticksList)) if sticksList[i] > 0]
        row = random.randint(0, len(nonEmptySticksList) - 1)
        move = random.randint(1, nonEmptySticksList[row][1])
        return (nonEmptySticksList[row][0] + 1, move)

    @staticmethod
    def level2(game):
        """Strategie für einen mittelmässigen Computerspieler."""
        sticksList = game.gamePanel
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
            return (maxIndex + 1, maxSticks if bool(countRowOne%2 == 0) ^ bool(game.lastOneLoses) else maxSticks - 1)
        # Sonst lassen wir 2 stehen oder wenn es nur 2 gibt, dann nehmen wir beide weg
        else:
            return (maxIndex + 1, maxSticks - 2 if maxSticks > 2 else 2)

    @staticmethod
    def level3(game):
        """Strategie für einen optimalen Computerspieler."""
        sticksList = game.gamePanel
        xorValue = reduce(lambda s, e: s ^ e, sticksList, 0)
        countRowMore = reduce(lambda s, e: s + 1 if e > 1 else s, sticksList, 0)
        countRowOne = reduce(lambda s, e: s + 1 if e == 1 else s, sticksList, 0)

        # In der Misère-Variante müssen wir schauen ob es nur noch eine Reihe mit mehr als 1 Stick gibt
        if game.lastOneLoses and countRowMore == 1:
            # ...dann nehmen wir hier alle oder alle bis auf 1 Sticks weg, abhängig davon
            # wie viele andere Reihen es noch gibt mit je einem Stick.
            longRow = [(i + 1, sticksList[i] - (countRowOne + 1)%2) for i in range(len(sticksList)) if sticksList[i] > 1]
            return longRow[0]
        # Wenn es nur noch 1-er Reihen gibt oder der XOR-Wert 0 ist (Verluststellung), dann
        # können wir einfach einen zufälligen Zug machen.
        elif countRowMore == 0 or xorValue == 0:
            return NimMulti.level1(game)
        # Ansonsten nehmen wir die erste Reihe, wo wir dem anderen Spieler eine Verlusstellung übergeben können
        else:
            for i in range(len(sticksList)):
                newNumberOfSticks = sticksList[i] ^ xorValue
                if newNumberOfSticks < sticksList[i]:
                    return (i + 1, sticksList[i] - newNumberOfSticks)
