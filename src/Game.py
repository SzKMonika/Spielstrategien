import os, sys, time

# -------------------- class Game --------------------
class Game(object):
    def __init__(self, player1, player2, printMoves = True):
        self.__playerCallback = (player1, player2)
        self.__playerName = (player1.__name__ + " (1)", player2.__name__ + " (2)")
        self._printMoves = printMoves
        self.__nextPlayer = 1
        self.__nextMove = 0
        self.__moveRecords = []

    def setPrintMoves(self, printMoves):
        self._printMoves = printMoves

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
        self.__recordState((self.nextMove, self.nextPlayer, " ", self.gamePanel))
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
        if self._printMoves:
            print(self.stateToString(state))

    def stateToString(self, state):
        """Gibt den Spielstand nach einem Zug in kompakter/ausdruckbarer Form zurück."""
        if (state[1] > 0):
            header = "{:2d}. Zug, Spieler {:d}: {} => ".format(state[0], state[1], state[2]) if state[0] > 0 else " START                => "
            s = self.gamePanelToString(state[3], header)
        elif state[1] < 0:
            s = " ENDE: {} gewinnt nach {:d} Zügen!".format(self.__playerName[-state[1]-1], state[0])
            if (state[2] != None):
                s += " Grund: Falscher Zug ({}) des anderen Spielers.".format(state[2])
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
        return "{} Spiel: {} gegen {}".format(type(self).__name__, self.__playerName[0], self.__playerName[1])

    def _getState(self, index):
        """Gibt den rohen Spielstand nach dem gewählten Zug zurück."""
        return self.__moveRecords[index % len(self.__moveRecords)]

    def getStateString(self, index):
        """Gibt den Spielstand als String nach dem gewählten Zug zurück."""
        return self.stateToString(self._getState(index))

# -------------------- Human player callback --------------------   
def human(game):
    """Ein Callback für einen menschlichen Spieler, der den Benutzer um ihren Zug fragt."""
    move = None
    exc = ""
    while move is None:
        try:
            #print(game.getStateString(-1) + "\n") TODO Hier ausschreiben statt in recordState, ab dem letzten eigenen Zug (Kalaha)
            move = eval(str(input(exc + str(game.nextMove) + ". Zug kommt, welchen Zug wählst du? ")))
            game.checkMove(move)
        except Exception as e:
            move = None
            exc = str(e) + "! "
    return move

# -------------------- Game execution --------------------   
IS_PYTHON3 = sys.version_info[0] > 2

IS_JYTHON = sys.executable.endswith("jython.exe") or sys.platform.startswith("java")

if IS_JYTHON:
    #from gpanel import *
    import gconsole
    println = gconsole.gprintln
    waitForKey = gconsole.getKeyCodeWait
    clr = gconsole.clear
else:
    import builtins
    import keyboard # pip3 install keyboard / https://stackoverflow.com/questions/24072790/how-to-detect-key-presses
    println = builtins.print
    waitForKey = keyboard.read_key
    clr = (lambda: os.system('clear')) if os.name == 'posix' else (lambda: os.system('cls')) # https://www.scaler.com/topics/how-to-clear-screen-in-python/

def playOne(createGame, player1, player2, printMoves = True):
    """Führt ein Spiel (Game) einmal aus und erlaubt es nachher die Schritte einzeln anzuschauen."""
    game = createGame(player1, player2)
    game.setPrintMoves(printMoves)
    game.play()
    if IS_JYTHON:
        gconsole.makeConsole()
    println("Benutze die Pfeiltasten um jeden Spielzug einzeln anzuschauen, und q um zu beenden!")
    keyPressed = waitForKey()
    index = 0
    while keyPressed != 'q' and keyPressed != 81:
        clr()
        println(game.getPlayerNames())
        println('')
        println(game.getStateString(index))
        time.sleep(0.2)
        keyPressed = waitForKey()
        if keyPressed == 37 or keyPressed == 'nach-links':
            index -= 1
        if keyPressed == 39 or keyPressed == 'nach-rechts':
            index += 1
        if keyPressed == 40 or keyPressed == 'nach-unten':
            index = 0
    if IS_JYTHON:
        gconsole.dispose()

def playMany(createGame, player1, player2, count = 100):
    """Führt ein Spiel (Game) mehrmals aus und gibt nachher eine Statistik aus."""
    game1stats = [0, 0, 0]
    game1wrongmove = [0, 0, 0]
    game2stats = [0, 0, 0]
    game2wrongmove = [0, 0, 0]
    if IS_JYTHON:
        gconsole.makeConsole()

    for i in range(1, count+1):
        game1 = createGame(player1, player2)
        game1.setPrintMoves(False)
        game1.play()
        winner = -game1._getState(-1)[1]
        game1stats[winner] += 1
        if game1._getState(-1)[2] != None:
            game1wrongmove[winner] += 1
        game2 = createGame(player2, player1)
        game2.setPrintMoves(False)
        game2.play()
        # Im game2 sind die Spieler umgekehrt, darum arbeiten wir einfach mit negativem Gewinner bzw. Index
        winner = game2._getState(-1)[1]
        game2stats[winner] += 1
        if game2._getState(-1)[2] != None:
            game2wrongmove[winner] += 1
        if IS_JYTHON:
            time.sleep(0.2)
        clr()
        println(game1.getPlayerNames() + " \n")
        println("  Erster Zug    |  Unentschieden  |    Spieler (1) gewinnt     |    Spieler (2) gewinnt")
        println("    durch       |                 | (davon wegen falschem Zug) | (davon wegen falschem Zug)")
        println("----------------+-----------------+----------------------------+----------------------------")
        println("  Spieler (1)   |      {:^5}      |           {:^5}            |           {:^5}".format(game1stats[0], game1stats[1], game1stats[2]))
        println("                |                 |          ({:^5})           |          ({:^5})".format(game1wrongmove[1], game1wrongmove[2]))
        println("----------------+-----------------+----------------------------+----------------------------")
        println("  Spieler (2)   |      {:^5}      |           {:^5}            |           {:^5}".format(game2stats[0], game2stats[1], game2stats[2]))
        println("                |                 |          ({:^5})           |          ({:^5})".format(game2wrongmove[1], game2wrongmove[2]))

    if IS_JYTHON:
        waitForKey()
        gconsole.dispose()
