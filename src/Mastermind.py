import random
from Game import human

# -------------------- class Mastermind --------------------
class Mastermind():
    def __init__(self, player1, player2):
        self.__numDigits = 4
        self.__secretNumber = random.randint(0, 10**self.__numDigits - 1)
        self.__guesser = player1
        self.__guessList = []
        self.__nextMove = 0
    
    @property
    def gamePanel(self):
        return list(self.__guessList)

    @property
    def nextMove(self):
        """Gibt zurück, wievielter Zug gerade kommt."""
        return self.__nextMove

    def play(self):
        """Startet das Spiel und ruft alternierend beide Spieler-Strategien auf, bis eine gewinnt."""
        try:
            match = False
            while not match:
                self.__nextMove += 1
                move = self.__guesser(self)
                self.checkMove(move)
                match = self._doMove(move)
                print(self.stateToString((self.nextMove, move, self.gamePanel)))
        except ValueError as e:
            pass #TODO Was tun wir beim Fehler?

    def checkMove(self, move):
        """Prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht."""
        if not isinstance(move, int):
            raise ValueError("Es muss eine ganze Zahl angegeben werden!")
        if move < 0 or move > 10**self.__numDigits - 1:
            raise ValueError("Es muss eine ganze Zahl zwischen 0 und " + str(10**self.__numDigits - 1) + " angegeben werden!")

    def _doMove(self, move):
        """Macht den aktuellen Zug und gibt zurück welcher Spieler als nächster kommt."""
        good, halfgood = compareNumbers(move, self.__secretNumber, self.__numDigits)
        #TODO Der andere Spieler soll good und halfgood angeben.
        # Der Spielpanel soll alle bisherige Tipps und dazu gehörige Resultate enthalten
        self.__guessList.append((move, good, halfgood))
        return good == self.__numDigits

    def stateToString(self, state):
        """Gibt den Spielstand nach einem Zug in kompakter/ausdruckbarer Form zurück."""
        return self.gamePanelToString(state[2], "{:2d}. Zug: {:4d} => ".format(state[0], state[1]))

    def gamePanelToString(self, gamePanel, firstLine = ""):
        s = ""
        for guess in gamePanel[::-1]:
            s += ("\n" + " "*len(firstLine) if len(s) > 0 else "") + "{:04d} : {:d} GUT + {:d} halbgut".format(guess[0], guess[1], guess[2])
        return firstLine + s + "\n"

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

        # Von den verbleibenden Zahlen wählen wir vollständig random
        next = random.randint(0, len(self.possibleSecretNumbers) - 1)
        print("Anzahl Möglichkeiten {}".format(len(self.possibleSecretNumbers)))
        return self.possibleSecretNumbers[next]

mastermind = lambda p1, p2: Mastermind(p1, p2)
strategy = MastermindStrategy()
#mastermind(strategy.Mastermind_L2, None).play()
mastermind(human, None).play()

#TODO playMany!