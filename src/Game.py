# -------------------- class Game --------------------
class Game(object):
    def __init__(self, player1, player2, player1name = "Spieler 1", player2name = "Spieler 2"):
        self.__playerCallback = (player1, player2)
        self.__playerName = (player1name, player2name)
        self.__nextPlayer = 1
        self.__nextMove = 0
        self.__moveRecords = []

    @property
    def nextPlayer(self):
        """Gibt den Spieler (1 oder 2) zurück, dessen Zug gerade kommt."""
        return self.__nextPlayer

    @property
    def nextMove(self):
        """Gibt zurück, wievielter Zug gerade kommt."""
        return self.__nextMove

    @property
    def gamePanel(self):
        """Das konkrete Spiel gibt das Spielfeld in seinem Rohform zurück."""
        return None

    def play(self):
        """Startet das Spiel und ruft alternierend beide Spieler-Strategien auf, bis eine gewinnt."""
        self.__recordState((self.nextMove, self.nextPlayer, "0", self.gamePanel))
        try:
            while self.__nextPlayer > 0:
                self.__nextMove += 1
                move = self.__playerCallback[self.__nextPlayer-1](self)
                self.checkMove(move)
                nextPlayer = self._doMove(move)
                self.__recordState((self.nextMove, self.nextPlayer, move, self.gamePanel))
                winner = self._checkEnd(move)
                if winner is None:
                    self.__nextPlayer = nextPlayer
                else:                    
                    self.__nextPlayer = -winner
                    self.__recordState((self.__nextMove, self.__nextPlayer, None, None))
        except ValueError as e:
            self.__nextPlayer = -(self.__nextPlayer%2 + 1)
            self.__recordState((self.__nextMove, self.__nextPlayer, move, None))

    def checkMove(self, move):
        """Prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht."""
        pass

    def _doMove(self, move):
        """Macht den aktuellen Zug und gibt zurück welcher Spieler als nächster kommt."""
        return 0

    def _checkEnd(self, move):
        """Gibt an ob das Spiel mit unentschieden beendet ist (0) oder ein Spieler gewonnen hat (1 oder 2), oder noch nicht beendet ist (None)"""
        return None

    def __recordState(self, state):
        """Speichert den Zug und den Spielstand ab um am Ende des Spiels den Spielablauf sehen zu können."""
        self.__moveRecords.append(state)
        print(self.stateToString(state)) # TODO: Löschen

    def stateToString(self, state):
        """Gibt den Spielstand nach einem Zug in kompakter/ausdruckbarer Form zurück."""
        if (state[1] > 0):
            s = self.gamePanelToString(state[3], "({:2d}/{:d}): {} => ".format(state[0], state[1], state[2]))
        elif state[1] < 0:
            s = " ENDE: {} ({:d}) gewinnt nach {:d} Zügen!".format(self.__playerName[-state[1]-1], -state[1], state[0])
            if (state[2] != None):
                s += " Grund: Falscher Zug ({:d}) des anderen Spielers.".format(state[2])
        else:
            s = " ENDE: Das Spiel endet unentschieden nach {:d} Zügen!".format(state[0])
        return s

    def gamePanelToString(self, gamePanel, firstLine = ""):
        """Gibt das gamePanel als String zurück. Diese Methode sollte von den Subklassen überschrieben werden."""
        return firstLine + str(gamePanel)

    def printAllStates(self):
        """Gibt alle Züge in kompakter Form aus."""
        for state in self.__moveRecords:
            print(self.stateToString(state))

    def getPlayerNames(self):
        """Gibt das Spiel und den Namen der gegeneinander antretenden Spieler/Strategien zurück."""
        return "{} Spiel: {} (1) gegen {} (2)".format(type(self).__name__, self.__playerName[0], self.__playerName[1])

    def getState(self, index):
        """Gibt den Spielstand als String nach dem gewählten Zug zurück."""
        return self.stateToString(self.__moveRecords[index % len(self.__moveRecords)])

# -------------------- Human player callback --------------------   
def human(game):
    """Ein Callback für einen menschlichen Spieler, der den Benutzer um ihren Zug fragt."""
    n = None
    exc = ""
    while n is None:
        try:
            n = eval(str(input(exc + str(game.nextMove) + ". Zug kommt, welchen Zug wählst du? ")))
            game.checkMove(n)
        except Exception as e:
            n = None
            exc = str(e) + "! "
    return n
