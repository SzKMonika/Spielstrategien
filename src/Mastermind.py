import os
import random
from Game import human

# -------------------- class Mastermind --------------------
class Mastermind():
    """Das ist ein eigenständiges Zweipersonen-Spiel, das jedoch asymmetrisch mit imperferkter Information ist.
    Wie im echten Mastermind, muss der erste Spieler eine geheime Reihenfolge ausdenken und der zweite Spieler muss diese erraten. Die Reihenfolge besteht
    in diesem Spiel aus Ziffern (0 bis 9) statt Farben (wie im echten Mastermind).
    Nach jedem Tipp gibt der erste Spieler dem zweiten an, wie viele Ziffern gut sind und an guter Stelle sich befinden, und wie viele an falscher Stelle sind.
    Wenn diese Resultat immer vom menschlichen Spieler zurückgegeben werden soll, dann sollte player1 = (lambda _: None) und guessResult = humanGuessResult sein.

    Args:
        player1: Eine Callback-Funktion die in play() einmalig aufgerufen wird, um die Geheimzahl zu ermitteln.
        player2: Eine Callback-Funktion die in play() aufgerufen wird, um die Züge (Tipps) des Spieler 2 zu ermitteln.
        guessResult: Eine Callback-Funktion vom Spieler 1, die zum eingegebenen Tipp die gute und halbgute Zifferzahl angibt. Bei Computer-Spielern kann es None sein.

    Attributes:
        __length (int): Die Anzahl Ziffern bzw. Dezimalstellen der Geheimzahl.
        __maxGuessLimit (int): Der maximale Anzahl Tipps, um Endlos-Schleifen zu vermeiden.
        __secretCreator: Die als player1 eingegebene Callback-Funktion oder wenn die None ist, dann eine Lambda-Funktion die eine random Zahl generiert.
        __guesser: Die als player2 eingegebene Callback-Funktion.
        __guessResult: Die als guessResult eingegebene Callback-Funktion.
        __guessList: Die Liste der Züge, die aus 3-er Tuplen besteht.
        __nextMove (int): Gibt an, welcher Zug kommt. Der erste Zug hat den Index 1.
    """
    def __init__(self, player1, player2, guessResult = None):
        self.__length = 4
        self.__maxGuessLimit = 50
        self.__secretCreator = player1 if player1 is not None else (lambda length: random.randint(0, 10**length - 1))
        self.__guesser = player2
        self.__guessResult = guessResult
        self.__guessList = []
        self.__nextMove = 0
    
    @property
    def gamePanel(self):
        """Das Spielfeld in seinem Rohmodell wird zurückgegeben, damit die Spieler-Callbacks daraus den Spielstand vollständig erkunden können.
        Das Spielfeld besteht - wie im echten Mastermind - aus Zeilen, und jede Zeile beinhaltet ein 3-er Tuple bestehend aus einem Tipp und zwei
        Zahlen: die erste Zahl bedeutet die Anzahl richtigen Ziffer an guter Stelle, und die zweite Zahl bedeutet die Anzahl Ziffer an falscher Stelle.
        Hinweis: Eigentlich wird hier eine Kopie zurückgegeben, damit der Spielstand von aussen unveränderbar bleibt.
        """
        return list(self.__guessList)

    @property
    def nextMove(self):
        """Gibt zurück, wievielter Zug gerade kommt, oder bei Spielende die Anzahl insgesamt gemachter Züge."""
        return self.__nextMove

    def play(self):
        """Startet das Spiel und ruft zuerst einmalig die Callback-Funktion vom Spieler 1 auf um die Geheimzahl zu ermitteln.
        Nachher wird die Spieler-Strategie vom Spieler 2 wiederholend aufgerufen, bis die Geheimzahl erraten wird oder wenn schon 100-mal geraten wurde.
        Die Züge werden in einer Schleife abgearbeitet, mit folgendem Ablauf:
        1. __nextMove wird um 1 erhöht und der __guesser Strategie-Callback wird aufgerufen. Dieser Antwortet mit einem 'move'.
        2. Der 'move' wird geprüft, ob er den Regeln entspricht. Falls nicht, dann gehen wir zurück zu Schritt 1.
        3. In _doMove() wird geprüft und zurückgegeben wie viele Ziffer ganz gut sind, und wie viele Ziffer sich an falscher Stelle befinden.
        4. Der aktuelle Spielstand wird via print() ausgegeben.
        """
        secretNumber = self.__secretCreator(self.__length)

        match = False
        while not match and self.__nextMove < self.__maxGuessLimit:
            try:
                self.__nextMove += 1
                move = self.__guesser(self)
                self.checkMove(move)
                match = self._doMove(move, secretNumber)
                print(self.stateToString((self.nextMove, move, self.gamePanel)))
            except ValueError as e:
                print("Ungültiger Tipp ({}): {}".format(move, str(e)))

    def checkMove(self, move):
        """Hier wird geprüft, ob die gewählte Zahl zwischen 0 und 9999 (10^4-1) ist.

        Raises:
            ValueError: Wenn die Eingabe keine ganze Zahl ist, oder negativ bzw. grösser als 9999 ist, wird ein ValueError mit entsprechendem Text geworfen.
        """
        if not isinstance(move, int):
            raise ValueError("Es muss eine ganze Zahl angegeben werden!")
        if move < 0 or move > 10**self.__length - 1:
            raise ValueError("Es muss eine ganze Zahl zwischen 0 und " + str(10**self.__length - 1) + " angegeben werden!")

    def _doMove(self, move, secretNumber):
        """In dieser Methode wird der eingegebene Tipp mit dem Geheimzahl verglichen, und der Tipp samt Vergleichsresultat dem __guessList hinzugefügt.
        Der Vergleich geschieht entweder durch die Funktion compareNumbers() oder durch menschlichen Input (via __guessResult).

        Returns:
            match (bool): True wenn die Geheimzahl erraten wurde, False wenn nicht.
        """
        if secretNumber is not None:
            good, halfgood = compareNumbers(move, secretNumber, self.__length)
        else:
            good, halfgood = self.__guessResult(move, self.__length)
        # Der Spielpanel soll alle bisherige Tipps und dazu gehörige Resultate enthalten
        self.__guessList.append((move, good, halfgood))
        return good == self.__length

    def stateToString(self, state):
        """Gibt den Spielstand nach einem Zug in kompakter/ausdruckbarer Form zurück."""
        return self.gamePanelToString(state[2], "{:2d}. Zug: {:4d} => ".format(state[0], state[1]))

    def gamePanelToString(self, gamePanel, firstLine = ""):
        """Das gamePanel wird als menschen-lesbarer String zurückgegeben."""
        s = ""
        for guess in gamePanel[::-1]:
            s += ("\n" + " "*len(firstLine) if len(s) > 0 else "") + "{:04d} : {:d} GUT + {:d} halbgut".format(guess[0], guess[1], guess[2])
        return firstLine + s + "\n"

    def _getLastStatesForNextPlayer(self):
        """Diese Methode wird für den 'human' Spieler gebraucht. Aktuell geben wir eine leere Liste zurück."""
        return []

# -------------------- Hilfsmethoden --------------------   
def compareNumbers(guess, secret, length = 4):
    """Vergleicht zwei Zahlen Ziffer für Ziffer und gibt zurück wie viele gute Ziffer an gleicher bzw. an unterschiedlicher Stelle sind.
    
    Returns:
        (good, halfgood): Ein 2-er Tuple, dessen erste Zahl die gute Ziffer an guter Stelle und die zweite Zahl die gute Ziffer an falscher Stelle angibt.
    """
    good = halfgood = 0
    guessNotGood = []
    secretNotGood = []

    # Zuerst iterieren wir durch alle Ziffer (von hinten) ...
    for _ in range(length):
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

# -------------------- Human player callbacks --------------------   
def humanSecretCreator(length):
    """Ein Callback für einen menschlichen Spieler, der den Benutzer um eine Geheimzahl fragt."""
    secret = None
    exc = ""
    while secret is None:
        try:
            secret = int(input("{} Gebe die Geheimzahl an: ".format(exc)))
            if secret < 0 or secret > 10**length - 1:
                raise ValueError("Es muss eine ganze Zahl zwischen 0 und {:d} angegeben werden!".format(10**length - 1))
        except Exception as e:
            secret = None
            exc = str(e) + "! "
    # Wir löschen die Konsole um die eingegebene Geheimzahl zu verbergen.
    os.system('clear' if os.name == 'posix' else 'cls') # https://www.scaler.com/topics/how-to-clear-screen-in-python/
    return secret

def humanGuessResult(guess, length):
    """Ein Callback für einen menschlichen Spieler, der den Benutzer um die gute und halbgute Ziffern fragt."""
    good = halfgood = None
    exc = ""
    while good is None or halfgood is None:
        try:
            good = int(input("{} Beim Tipp {:04d}, wie viele Ziffern sind gut und an GUTER Stelle? ".format(exc, guess)))
            if good < 0 or good > length:
                raise ValueError("Es muss eine ganze Zahl zwischen 0 und {:d} angegeben werden!".format(length))
            halfgood = int(input("{} Beim Tipp {:04d}, wie viele Ziffern sind gut und an falscher Stelle? ".format(exc, guess)))
            if halfgood < 0 or halfgood > length:
                raise ValueError("Es muss eine ganze Zahl zwischen 0 und {:d} angegeben werden!".format(length))
            if good + halfgood > length:
                raise ValueError("Die Summe der GUTEN und halbguten Ziffern darf nicht mehr als {:d} sein!".format(length))
        except Exception as e:
            good = halfgood = None
            exc = str(e) + "! "
    return (good, halfgood)

# -------------------- Class MastermindStrategy --------------------   
class MastermindStrategy:
    """Diese Klasse implementiert eine relativ gute Strategie für das Mastermind-Spiel. Sie führt eine Liste über die möglichen Geheimzahl-Kandidaten,
    die noch in Frage kommen können. Sinn und Zweck dieser Klasse ist, dass man in den vorherigen Schritten schon ausgeschiedenen Kandidaten festhält
    und nicht bei jedem Zug von vorne neu kalkuliert, da in jedem Zug etwa 80-90% der noch verbleibenden möglichen Zahlen ausscheiden.
    (Falls wir die noch möglichen Kandidaten nicht zwischenspeichern würden, würden die Spiele mit dieser Strategie mehr als zweimal länger dauern.)

    Attributes:
        possibleSecretNumbers: Liste der noch möglichen Geheimzahl-Kandidaten.
        lastGuessIndex (int): Hier merken wir, bis welchem Zug wir zuletzt die Kandidaten schon überprüft haben.
    """
    def __init__(self):
        self.possibleSecretNumbers = [i for i in range(10**4)]
        self.lastGuessIndex = 0

    def reset(self):
        """Die zwischengespeicherten Daten zurücksetzen, im Falle eines neuen Spiels."""
        self.possibleSecretNumbers[:] = [i for i in range(10**4)]
        self.lastGuessIndex = 0

    def Mastermind_L2(self, game):
        """Diese Methode ist die eigentliche Callback-Funktion, die dem Mastermind Spiel als Argument eingegeben werden soll."""
        guessList = game.gamePanel
        # Prüfen wir ob vielleicht ein neues Spiel gestartet wurde
        if game.nextMove < self.lastGuessIndex + 1:
            self.reset()

        # Wir prüfen die früher noch nicht geprüften Tipps...
        for i in range(self.lastGuessIndex, len(guessList)):
            guess = guessList[i]
            # ...und reduzieren die Liste der möglichen Geheimzahlen so, dass nur die Zahlen bleiben, die das gleiche Resultat geben würden.
            self.possibleSecretNumbers[:] = [number for number in self.possibleSecretNumbers if compareNumbers(guess[0], number) == (guess[1], guess[2])]

        self.lastGuessIndex = len(guessList)

        # Von den verbleibenden Zahlen wählen wir vollständig random
        if len(self.possibleSecretNumbers) > 0:
            next = random.randint(0, len(self.possibleSecretNumbers) - 1)
        else:
            raise ValueError("Der andere Spieler hat geschummelt! Ich bin raus!")
        #print("Anzahl Möglichkeiten {}".format(len(self.possibleSecretNumbers)))
        return self.possibleSecretNumbers[next]

strategy = MastermindStrategy()
game = Mastermind((lambda _: None), strategy.Mastermind_L2, humanGuessResult)
#game = Mastermind(humanSecretCreator, human, humanGuessResult)
#mastermind(None, human).play()
game.play()

#TODO playMany!