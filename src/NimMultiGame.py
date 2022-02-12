from Game import Game, human
import random

# -------------------- class NimMultiGame --------------------
class NimMultiGame(Game):
    def __init__(self, player1, player2, sticksList, lastOneLoses = False):
        super(NimMultiGame, self).__init__(player1, player2)
        self.__sticksList = sticksList
        self.__lastOneLoses = lastOneLoses

    @property
    def gamePanel(self):
        return list(self.__sticksList)    

    @property
    def lastOneLoses(self):
        return self.__lastOneLoses

    def checkMove(self, move):
        """Prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht."""
        if not isinstance(move, tuple):
            raise ValueError("Es müssen zwei mit Komma getrennten ganze Zahlen angegeben werden!")
        if move[0] < 1 or move[0] > len(self.__sticksList):
            raise ValueError("Gewählte Reihe " + str(move[0]) + " ist ungültig!")
        if move[1] < 1 or move[1] > self.__sticksList[move[0]-1]:
            raise ValueError("In der gewählten Reihe " + str(move[0]) + " wollte man eine ungültige Anzahl " + str(move[1]) + " wegnehmen!")

    def _doMove(self, move):
        """Macht den aktuellen Zug und gibt zurück welcher Spieler als nächster kommt."""
        self.__sticksList[move[0]-1] = self.__sticksList[move[0]-1] - move[1]
        return (self.nextPlayer % 2 + 1)

    def _checkEnd(self, move):
        """Gibt an ob das Spiel mit unentschieden beendet ist (0) oder ein Spieler gewonnen hat (1 oder 2), oder noch nicht beendet ist (None)"""
        return None if sum(self.__sticksList) > 0 else (self.nextPlayer%2+1) if self.__lastOneLoses else self.nextPlayer

# -------------------- Computer player callbacks --------------------   
def NimMulti_L1(game):
    """Callback für einen dummen Computerspieler."""
    sticksList = game.gamePanel
    nonEmptySticksList = [(i, sticksList[i]) for i in range(len(sticksList)) if sticksList[i] > 0]
    row = random.randint(0, len(nonEmptySticksList)-1)
    move = random.randint(1, nonEmptySticksList[row][1])
    return (nonEmptySticksList[row][0] + 1, move)

def NimMulti_L2(game):
    """Callback für einen mittelmässigen Computerspieler."""
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
        return (maxIndex + 1, maxSticks if bool(countRowOne % 2 == 0) ^ bool(game.lastOneLoses) else maxSticks-1)
    # Sonst lassen wir 2 stehen oder wenn es nur 2 gibt, dann nehmen wir beide weg
    else:
        return (maxIndex + 1, maxSticks-2 if maxSticks > 2 else 2)

#-------------MAIN
nimGame = NimMultiGame(human, NimMulti_L2, [1,3,5,7])
nimGame.play()
