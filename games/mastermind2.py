"""Dieses Modul beinhaltet die Klasse Mastermind2, eine konkrete Subklasse von Game."""

from games.game import Game
from games.mastermind import Mastermind, MastermindStrategy
import random

# -------------------- class Mastermind2 --------------------
class Mastermind2(Game):
    """Das ist ein modifiziertes Mastermind-Spiel, das durch Game symmetrisch gemacht wurde. Am Anfang wird eine zufällige Geheimzahl generiert,
    und diese muss abwechselnd von den beiden Spielern erraten werden. Derjenige Spieler, der die Geheimzahl zuerst errät, gewinnt.
    Nach jedem Tipp wird angegeben, wie viele Ziffern richtig sind und an guter Stelle sich befinden (gut), und wie viele an falscher Stelle sind (halbgut).
    Unten werden nur die Mastermind2-spezifische Argumente und Attribute aufgeführt, für die sonstigen bitte im Game schauen.
    Hinweis: Einige der Methoden, insbesondere für die Strategien verwenden die Methoden der Klasse Mastermind wieder.

    Attributes:
        __length (int): Die Anzahl Ziffern bzw. Dezimalstellen der Geheimzahl.
        __secretNumber (int): Die zu erratende Geheimzahl.
        __guessList: Die Liste der Züge, die jeweils aus 3-er Tuplen bestehen: (Tipp, Gut, Halbgut)
    """
    def __init__(self, player1, player2):
        super(Mastermind2, self).__init__(player1, player2)
        self.__length = 4
        self.__secretNumber = random.randint(0, 10**self.__length - 1)
        self.__guessList = []
    
    @property
    def gamePanel(self):
        return list(self.__guessList)

    def checkMove(self, move):
        if not isinstance(move, int):
            raise ValueError("Es muss eine ganze Zahl angegeben werden!")
        if move < 0 or move > 10**self.__length - 1:
            raise ValueError("Es muss eine ganze Zahl zwischen 0 und " + str(10**self.__length - 1) + " angegeben werden!")

    def _doMove(self, move):
        good, halfgood = Mastermind.compareNumbers(move, self.__secretNumber, self.__length)
        # Der Spielpanel soll alle bisherige Tipps und dazu gehörige Resultate enthalten
        self.__guessList.append((move, good, halfgood))
        return (self.nextPlayer%2 + 1)

    def _checkEnd(self, move):
        return None if move != self.__secretNumber else self.nextPlayer

    def gamePanelToString(self, gamePanel, firstLine = ""):
        s = ""
        for guess in gamePanel[::-1]:
            s += ("\n" + " "*len(firstLine) if len(s) > 0 else "") + "{:04d} : {:d} GUT + {:d} halbgut".format(guess[0], guess[1], guess[2])
        return firstLine + s + "\n"

    # -------------------- Hilfsmethoden --------------------   
    @staticmethod
    def compareNumbers(guess, secret, numDigits = 4):
        """Vergleicht zwei Zahlen Ziffer für Ziffer und gibt zurück wie viele gleiche Ziffer an gleicher bzw. an unterschiedlicher Stelle sind."""
        return Mastermind.compareNumbers(guess, secret, numDigits)

    # -------------------- Computer Strategien --------------------   
    @staticmethod
    def level2(game):
        """Strategie für einen mittelmässigen Computerspieler, der mit den Ziffern einzeln arbeitet."""
        return Mastermind.player2_level2(game)

    @staticmethod
    def level3_():
        """Gibt die gute Strategie von MastermindStrategy zurück."""
        return Mastermind.player2_level3_()
