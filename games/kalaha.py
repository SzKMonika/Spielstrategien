"""Dieses Modul beinhaltet die Klasse Kalaha, eine konkrete Subklasse von Game."""

from games.game import Game
import copy, random

# -------------------- class Kalaha --------------------
class Kalaha(Game):
    """Das ist ein konkretes Spiel (Game), in dem das Ziel ist, mehr Steine auf der eigenen Seite zu sammeln als der Gegner.
    Das Spielbrett besteht aus zwei Muldenreihen mit jeweils sechs Spielmulden plus eine Gewinnmulde jeweils auf der rechten Seite des Spielers.
    Am Anfang legt man in jede Spielmulde 4 Steine. Die Spieler bewegen die Steine so, dass aus einer eigenen Spielmulde alle Steine genommen werden,
    und diese gegen Uhrzeigersinn auf die folgenden Mulden verteilt werden (ausser gegnerische Gewinnmulde). Wenn der letzte Stein in der eigenen
    Gewinnmulde landet gibt es einen Bonus-Zug, sonst kommt der andere Spieler.
    Es gibt noch einen Spezialfall: Wenn der letzte Stein in einer eigenen leeren Spielmulde landet, und direkt gegenüber 1 oder mehrere Steine
    liegen, dann werden alle Steine aus beiden Mulden in die eigene Gewinnmulde verschoben
    Das Spiel endet wenn nach einem Zug die Spielmulden auf einer Seite ganz leer werden.
    Es gewinnt derjenige Spieler, der mehr Steine auf seiner Seite (inkl. Gewinnmulde) gesammelt hat, bei Gleichstand ist es unentschieden.
    Unten werden nur die Kalaha-spezifische Argumente und Attribute aufgeführt, für die sonstigen bitte im Game schauen.

    Attributes:
        __PITS (int): Anzahl Spielmulden pro Spieler (Konstante mit dem Wert 6).
        __pit: Das Spielbrett-Modell. Es besteht aus einer Tuple mit 2 Listen (für die zwei Muldenreihen) mit jeweils 7 ganzen Zahlen.
                Beide Listen haben auf Index 0 die Anzahl Steine in der Gewinnmulde, und unter Index 1 bis 6 befinden sich die Anzahl Steine
                in den Spielmulden, und zwar immer von der Gewinnmulde gezählt. 
    """
    __PITS = 6
    def __init__(self, player1, player2):
        super(Kalaha, self).__init__(player1, player2)
        stones = 4
        self.__pit = ([0] + [stones]*self.__PITS, [0] + [stones]*self.__PITS)

    @property
    def gamePanel(self):
        return copy.deepcopy(self.__pit)

    def checkMove(self, move):
        if not isinstance(move, int):
            raise ValueError("Es muss eine ganze Zahl angegeben werden!")
        if move < 1 or move > self.__PITS:
            raise ValueError("Gewählte Mulde " + str(move) + " ist ungültig!")
        if self.__pit[self.nextPlayer - 1][move] < 1:
            raise ValueError("In der gewählten Mulde " + str(move) + " gibt es keinen Stein!")

    def _doMove(self, move):
        # Zuerst entfernen wir alle Steine von der gewählten Mulde
        stones = self.__pit[self.nextPlayer - 1][move]
        self.__pit[self.nextPlayer - 1][move] = 0
        # Dann verteilen wir die Steine rekursiv auf die nächsten Mulden
        nextPlayer = self.__addStone(self.nextPlayer - 1, move - 1, stones)
        return nextPlayer

    def _checkEnd(self, move):
        if sum(self.__pit[0][1:]) < 1 or sum(self.__pit[1][1:]) < 1:
            stones1 = sum(self.__pit[0])
            stones2 = sum(self.__pit[1])
            return 1 if stones1 > stones2 else 2 if stones1 < stones2 else 0
        return None

    def __addStone(self, row, pit, remaining):
        """Addiert 'remaining' Anzahl Steine angefangen von der gegebenen Mulde 'pit' in der gegebenen Zeile 'row', rekursiv."""
        if remaining < 1:
            # Nachdem alle Steine verteilt wurden, kommt der andere Spieler an der Reihe
            return self.nextPlayer%2 + 1
        elif pit < 1:
            # In der eigener Reihe legen wir einen zusätzlichen Stein auch in den Kalah
            if row == self.nextPlayer - 1:
                self.__pit[row][0] += 1
                remaining -= 1
                # Wenn das der letzte Stein war, dann kommt nochmals dieser Spieler
                if remaining < 1:
                    return self.nextPlayer
            # Sonst springen wir rüber auf die andere Reihe, zur letzten Mulde
            return self.__addStone((row + 1)%2, self.__PITS, remaining)
        else:
            # Wir legen einfach einen Stein ab in die aktuelle Mulde
            self.__pit[row][pit] += 1
            remaining -= 1
            if remaining < 1:
                stonesInOppositePit = self.__pit[(row + 1)%2][self.__PITS + 1 - pit]
                # Wenn das der letzte Stein war und in eine eigene leere Mulde gestellt wurde,
                # deren gegenüberliegende Mulde nicht leer war, dann ...
                if row == self.nextPlayer - 1 and self.__pit[row][pit] == 1 and stonesInOppositePit > 0:
                    # ... speichern wir den Zwischenstand für bessere Nachvollziehbarkeit
                    # TODO? self.__recordState((self.__nextMove, self.__nextPlayer, "*", copy.deepcopy(self.__pit)))
                    # ... und verschieben alle Steine der beiden Mulden in den eigenen Kalah
                    self.__pit[row][0] += stonesInOppositePit + 1
                    self.__pit[row][pit] = 0
                    self.__pit[(row + 1)%2][self.__PITS + 1 - pit] = 0
                # Nachdem alle Steine verteilt wurden, kommt der andere Spieler an der Reihe
                return self.nextPlayer%2 + 1
            # Wenn das nicht der letzte Stein war, gehen wir weiter zur nächsten Mulde
            else:
                return self.__addStone(row, pit - 1, remaining)

    def getPitListForNextPlayer(self):
        """Gibt den Inhalt der Muldenreihe des aktuellen Spielers als eine Liste von Zahlen zurück, wenn das Spiel noch läuft.
        Auf Index 0 ist die Gewinnmulde, und auf Index 1 bis 6 sind die Anzahl Steine in den Spielmulden."""
        return list(self.__pit[self.nextPlayer - 1]) if self.nextPlayer > 0 else None

    def getPitListForOtherPlayer(self):
        """Gibt den Inhalt der Muldenreihe des anderen Spielers als eine Liste von Zahlen zurück, wenn das Spiel noch läuft.
        Auf Index 0 ist die Gewinnmulde, und auf Index 1 bis 6 sind die Anzahl Steine in den Spielmulden."""
        return list(self.__pit[self.nextPlayer%2]) if self.nextPlayer > 0 else None

    def gamePanelToString(self, gamePanel, firstLine = ""):
        pits1 = ["{:2d}".format(i) for i in gamePanel[0]]
        pits2 = ["{:2d}".format(i) for i in gamePanel[1][::-1]]
        return firstLine + " | ".join(pits1) + " |" + "\n" + " "*len(firstLine) + "   | " + " | ".join(pits2)

    # -------------------- Computer Strategien --------------------   
    @staticmethod
    def level1(game):
        """Strategie für einen dummen Computerspieler."""
        pitList = game.getPitListForNextPlayer()
        nonEmptyPitList = [i for i in range(len(pitList)) if i > 0 and pitList[i] > 0]
        return nonEmptyPitList[random.randint(0, len(nonEmptyPitList) - 1)]

    @staticmethod
    def level2a(game):
        return Kalaha._level2(game, 2)

    @staticmethod
    def level2b(game):
        return Kalaha._level2(game, 3)

    @staticmethod
    def level2c(game):
        return Kalaha._level2(game, 4)

    @staticmethod
    def _level2(game, startMoveValue = 4):
        """Parametrisierbare Strategie für einen halbwegs smarten Computerspieler.
        Je höher der 'startMoveValue' Parameter, desto mehr wird zufällig gezogen, wenn es keine Möglichkeit zum Bonus-Zug oder Fangen gibt."""
        myPitList = game.getPitListForNextPlayer()
        otherPitList = game.getPitListForOtherPlayer()
        move = Kalaha.level1(game)
        moveValue = startMoveValue
        for i in range(1, len(myPitList)):
            stones = myPitList[i]
            if stones > 0:
                # Zuerst schauen wir, ob es ein Zug gibt, der den letzten Stein gerade in Kalah bringt
                if i == stones:
                    return i
                # Sonst schauen wir, ob wir gegnerische Steine fangen können
                elif stones < i and myPitList[i - stones] == 0 and otherPitList[7 - i + stones] > 0:
                    return i
                elif stones > i + 6 and stones < 13 and myPitList[i + 13 - stones] == 0:
                    return i
                elif stones == 13:
                    return i
                # Wir schauen auf die andere Seite ob die Mulde dort leer ist und wir mehr als 'moveValue' Steine hier haben
                elif otherPitList[7 - i] == 0 and stones > moveValue:
                    move = i
                    moveValue = stones
                # Sonst suchen wir den Zug, der die wenigsten Steine auf die andere Seite bringt
                elif i - stones > moveValue:
                    move = i
                    moveValue = i - stones
        # Den move-Zug geben wir aber nur dann zurück, wenn wir sonst keinen anderen guten Zug haben
        return move

    @staticmethod
    def level3(game):
        """Strategie für einen ziemlich smarten Computerspieler."""
        myPitList = game.getPitListForNextPlayer()
        otherPitList = game.getPitListForOtherPlayer()
        move = 0
        moveValue = -50
        for i in range(1, len(myPitList)):
            stones = myPitList[i]
            if stones > 0:
                # Zuerst schauen wir, ob es ein Zug gibt, der den letzten Stein gerade in Kalah bringt
                if i == stones:
                    return i
                # Sonst schauen wir, ob wir gegnerische Steine erbeuten können
                elif stones < i and myPitList[i - stones] == 0 and otherPitList[7 - i + stones] > 0:
                    return i
                elif stones > i + 6 and stones < 13 and myPitList[i + 13 - stones] == 0:
                    return i
                elif stones == 13:
                    return i
                # Wir schauen auf die andere Seite, ob die Mulde dort leer ist oder so entleert werden kann, dass der Gegner wieder kommt
                elif otherPitList[7 - i] in (0, 7 - i) and stones > moveValue:
                    # In diesem Fall "retten" wir unsere Steine aus der Mulde, es sei denn...
                    move = i
                    moveValue = stones
                    defenseValue = i - stones
                    # ...wir könnten evtl. in die gegenüberliegende leere Mulde ein Stein "legen"
                    for j in range(1, len(myPitList)):
                        stones2 = myPitList[j]
                        if i != j and stones2 >= j + i and j - stones2 > defenseValue:
                            move = j
                            defenseValue = j - stones2              
                # Sonst suchen wir den Zug, der die wenigsten Steine auf die andere Seite bringt
                elif i - stones > moveValue:
                    move = i
                    moveValue = i - stones

        # Den move-Zug geben wir aber nur dann zurück, wenn wir sonst keinen anderen guten Zug haben
        return move
