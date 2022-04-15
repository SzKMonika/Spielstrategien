from Game import *
import random

# -------------------- class Mastermind --------------------
class Mastermind(Game):
    def __init__(self, player1, player2):
        super(Mastermind, self).__init__(player1, player2)
        self.__numDigits = 4
        self.__secretNumber = random.randint(0, 10**self.__numDigits - 1)
        self.__guessList = []
    
    @property
    def gamePanel(self):
        return list(self.__guessList)

    def checkMove(self, move):
        """Prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht."""
        if not isinstance(move, int):
            raise ValueError("Es muss eine ganze Zahl angegeben werden!")
        if move < 0 or move > 10**self.__numDigits - 1:
            raise ValueError("Es muss eine ganze Zahl zwischen 0 und " + str(10**self.__numDigits - 1) + " angegeben werden!")

    def _doMove(self, move):
        """Macht den aktuellen Zug und gibt zurück welcher Spieler als nächster kommt."""
        good, halfgood = compareNumbers(move, self.__secretNumber, self.__numDigits)
        # Der Spielpanel soll alle bisherige Tipps und dazu gehörige Resultate enthalten
        self.__guessList.append((move, good, halfgood))
        return (self.nextPlayer%2 + 1)

    def _checkEnd(self, move):
        """Gibt an ob das Spiel mit unentschieden beendet ist (0) oder ein Spieler gewonnen hat (1 oder 2), oder noch nicht beendet ist (None)"""
        return None if move != self.__secretNumber else self.nextPlayer

# -------------------- Hilfsmethoden --------------------   
def compareNumbers(guess, secret, numDigits = 4):
    """Vergleicht zwei Zahlen Ziffer für Ziffer und gibt zurück wie viele gleiche Ziffer an gleicher bzw. an unterschiedlicher Stelle sind."""
    good = halfgood = 0
    guessNotGood = []
    secretNotGood = []

    # Zuerst iterieren wir durch alle Ziffer (von hinten) ...
    for _ in range(numDigits):
        guessDigit = guess%10
        guess = guess//10
        secretDigit = secret%10
        secret = secret//10
        # ... und prüfen ob die Ziffer vom Tipp und Geheimzahl gleich sind
        if guessDigit == secretDigit:
            good = good + 1
        else:
            # Falls nicht, dann müssen wir nachher die Ziffer, die an falschen Stelle sind, prüfen
            guessNotGood.append(guessDigit)
            secretNotGood.append(secretDigit)

    # Wir iterieren durch alle Ziffer (digit) der Geheimzahl, die nicht an guter Stelle waren
    for digit in secretNotGood:
        try:
            # Schauen wir ob der Ziffer (digit) unter den Ziffern des Tipps vorkommt
            j = guessNotGood.index(digit)
            # Wir haben 'digit' in moveNotGood gefunden auf dem Index j, also entfernen wir es
            guessNotGood.pop(j)
            halfgood = halfgood + 1
        except ValueError:
            # Wir haben 'digit' in moveNotGood nicht gefunden, kein Problem
            pass

    return (good, halfgood)

# -------------------- TODO Main --------------------   
class MastermindStrategy:
    def __init__(self):
        self.possibleSecretNumbers = [i for i in range(10**4)]
        self.nextGuessIndex = 0

    def reset(self):
        """Die zwischengespeicherte Daten zurücksetzen, im Falle eines neuen Spiels."""
        self.possibleSecretNumbers[:] = [i for i in range(10**4)]
        self.nextGuessIndex = 0

    def Mastermind_L2(self, game):
        """Strategie für einen relativ guten brute-force Computerspieler, der die möglichen Lösungen zwischen den Zügen zwischenspeichert."""
        guessList = game.gamePanel
        # Prüfen wir ob vielleicht ein neues Spiel gestartet wurde
        if game.nextMove < self.nextGuessIndex + 1:
            self.reset()

        # Wir prüfen die früher noch nicht geprüften Tipps...
        for i in range(self.nextGuessIndex, len(guessList)):
            guess = guessList[i]
            # ...und reduzieren die Liste der möglichen Geheimzahlen so, dass nur die Zahlen bleiben, die das gleiche Resultat geben würden.
            self.possibleSecretNumbers[:] = [number for number in self.possibleSecretNumbers if compareNumbers(guess[0], number) == (guess[1], guess[2])]

        self.nextGuessIndex = len(guessList)
        print("({:2d}/{:d}): Strategie {} / {}".format(game.nextMove, game.nextPlayer, len(self.possibleSecretNumbers), self.nextGuessIndex))

        # Von den verbleibenden Zahlen wählen wir vollständig random
        next = random.randint(0, len(self.possibleSecretNumbers) - 1)
        return self.possibleSecretNumbers[next]

mastermind = lambda p1, p2: Mastermind(p1, p2)
strategy1 = MastermindStrategy()
strategy2 = MastermindStrategy()
playOne(mastermind, strategy1.Mastermind_L2, human)
#playMany(mastermind, strategy1.Mastermind_L2, strategy2.Mastermind_L2, 100)