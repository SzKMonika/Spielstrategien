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
        guess = move
        secret = self.__secretNumber
        good = halfgood = 0
        moveNotGood = []
        secretNotGood = []

        # Zuerst iterieren wir durch alle Ziffer (von hinten) ...
        for _ in range(self.__numDigits):
            moveDigit = guess%10
            guess = guess//10
            secretDigit = secret%10
            secret = secret//10
            # ... und prüfen ob die Ziffer vom Tipp und Geheimzahl gleich sind
            if moveDigit == secretDigit:
                good = good + 1
            else:
                # Falls nicht, dann müssen wir nachher die Ziffer, die an falschen Stelle sind, prüfen
                moveNotGood.append(moveDigit)
                secretNotGood.append(secretDigit)
        
        # Wir iterieren durch alle Ziffer (digit) der Geheimzahl, die nicht an guter Stelle waren
        for digit in secretNotGood:
            try:
                j = moveNotGood.index(digit)
                # Wir haben 'digit' in moveNotGood gefunden auf dem Index j, also entfernen wir es
                moveNotGood.pop(j)
                halfgood = halfgood + 1
            except ValueError:
                # Wir haben 'digit' in moveNotGood nicht gefunden, kein Problem
                pass

        # Der Spielpanel soll alle bisherige Tipps und dazu gehörige Resultate enthalten
        self.__guessList.append((move, good, halfgood))
        return (self.nextPlayer%2 + 1)

    def _checkEnd(self, move):
        """Gibt an ob das Spiel mit unentschieden beendet ist (0) oder ein Spieler gewonnen hat (1 oder 2), oder noch nicht beendet ist (None)"""
        return None if move != self.__secretNumber else self.nextPlayer

# -------------------- TODO Main --------------------   

mastermind = lambda p1, p2: Mastermind(p1, p2)
playOne(mastermind, human, human)
