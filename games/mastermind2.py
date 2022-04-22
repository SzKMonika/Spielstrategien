from games.game import Game
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
        good, halfgood = Mastermind.compareNumbers(move, self.__secretNumber, self.__numDigits)
        # Der Spielpanel soll alle bisherige Tipps und dazu gehörige Resultate enthalten
        self.__guessList.append((move, good, halfgood))
        return (self.nextPlayer%2 + 1)

    def _checkEnd(self, move):
        """Gibt an ob das Spiel mit unentschieden beendet ist (0) oder ein Spieler gewonnen hat (1 oder 2), oder noch nicht beendet ist (None)"""
        return None if move != self.__secretNumber else self.nextPlayer

    def gamePanelToString(self, gamePanel, firstLine = ""):
        """Das gamePanel wird als menschen-lesbarer String zurückgegeben."""
        s = ""
        for guess in gamePanel[::-1]:
            s += ("\n" + " "*len(firstLine) if len(s) > 0 else "") + "{:04d} : {:d} GUT + {:d} halbgut".format(guess[0], guess[1], guess[2])
        return firstLine + s + "\n"

    # -------------------- Hilfsmethoden --------------------   
    @staticmethod
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

    # -------------------- Computer Strategien --------------------   
    @staticmethod
    def level2(game):
        """Strategie für einen mittelmässigen Computerspieler, der mit den Ziffern einzeln arbeitet."""
        length = 4
        guessList = game.gamePanel
        # Wir erlauben am Anfang alle Ziffer an jeder Stelle
        possibleDigits = [[d for d in range(10)] for _ in range(length)]
        # Wir gehen durch alle Tipps, und...
        for i in range(len(guessList)):
            guess, good, halfgood = guessList[i]
            guessDigits = list(map(int, "{:04d}".format(guess)))
            #...wenn der Tipp komplett falsch war, dann löschen wir alle Ziffer des Tipps von allen Stellen.
            if good + halfgood == 0:
                possibleDigits = [[d for d in possibleDigits[i] if d not in guessDigits] for i in range(length)]
            #...wenn es keine ganz gute Ziffer gab, dann löschen wir die Ziffer des Tipps von den gleichen Stellen.
            elif good == 0:
                possibleDigits = [[d for d in possibleDigits[i] if d != guessDigits[i]] for i in range(length)]
            #...wenn alle Ziffer erraten wurden, dann löschen wir alle weiteren Ziffer von allen Stellen.
            elif good + halfgood == 4:
                possibleDigits = [[d for d in possibleDigits[i] if d in guessDigits] for i in range(length)]

        #print("possibleDigits = " + str(possibleDigits))
        newGuess = 0
        # Schlussendlich generieren wir eine Zufallszahl, Ziffer für Ziffer
        for i in range(length):
            newGuess *= 10
            newGuess += possibleDigits[i][random.randint(0, len(possibleDigits[i]) - 1)]
        return newGuess

    @staticmethod
    def level3p():
        """Gibt die gute Strategie von MastermindStrategy zurück."""
        strategy = MastermindStrategy()
        return strategy.level3

# -------------------- Class MastermindStrategy --------------------   
class MastermindStrategy:
    def __init__(self):
        self.possibleSecretNumbers = [i for i in range(10**4)]
        self.lastGuessIndex = 0

    def reset(self):
        """Die zwischengespeicherte Daten zurücksetzen, im Falle eines neuen Spiels."""
        self.possibleSecretNumbers = [i for i in range(10**4)]
        self.lastGuessIndex = 0

    def level3(self, game):
        """Strategie für einen relativ guten brute-force Computerspieler, der die möglichen Lösungen zwischen den Zügen zwischenspeichert."""
        guessList = game.gamePanel
        # Prüfen wir ob vielleicht ein neues Spiel gestartet wurde
        if game.nextMove < self.lastGuessIndex + 1:
            self.reset()

        # Wir prüfen die früher noch nicht geprüften Tipps...
        for i in range(self.lastGuessIndex, len(guessList)):
            guess = guessList[i]
            # ...und reduzieren die Liste der möglichen Geheimzahlen so, dass nur die Zahlen bleiben, die das gleiche Resultat geben würden.
            self.possibleSecretNumbers[:] = [number for number in self.possibleSecretNumbers if Mastermind.compareNumbers(guess[0], number) == (guess[1], guess[2])]

        self.lastGuessIndex = len(guessList)
    
        # Von den verbleibenden Zahlen wählen wir vollständig random
        if len(self.possibleSecretNumbers) > 0:
            next = random.randint(0, len(self.possibleSecretNumbers) - 1)
        else:
            raise ValueError("Der andere Spieler hat geschummelt! Ich bin raus!")
        #print("Anzahl Möglichkeiten {}".format(len(self.possibleSecretNumbers)))
        return self.possibleSecretNumbers[next]
