import os, sys, time

# -------------------- class Game --------------------
class Game(object):
    """Die Game Klasse ist die gemeinsame Hauptklasse für alle Zweipersonen-Spiele und ist somit der Kern des Frameworks.
    Hier wird der Ablauf der Spiele generell definiert (siehe play()). Manche Methoden (wie checkMove(), _doMove() und _checkEnd())
    müssen in den konkreten Spielklassen überschrieben bzw. implementiert werden.

    Args:
        player1: Eine Callback-Funktion die in play() aufgerufen wird, um die Züge des Spieler 1 zu ermitteln.
        player2: Eine Callback-Funktion die in play() aufgerufen wird, um die Züge des Spieler 2 zu ermitteln.
        printMoves (bool): Gibt an, ob die einzelne Züge während des Spiels via print() ausgeschrieben werden sollen, oder nicht

    Attributes:
        __playerCallback: Ein Tuple aus den eingegeben player1 und player2 Callback-Funktionen.
        __playerName: Ein Tuple, das die Namen der player1 und player2 Callback-Funktionen und somit den zugewiesenen Spielernamen enthält.
        _printMoves (bool): Der Wert vom printMoves Argument.
        __nextPlayer (int): Gibt an, welcher Spieler gerade am Zug ist (1 oder 2). Bei Spielende wird es 0 bei unentschieden bzw. -1 oder -2 abhängig davon wer gewonnen hat.
        __nextMove (int): Gibt an, welcher Zug kommt. Der erste Zug hat den Index 1.
        __moveRecords: Eine Liste, die für den Startzustand, für jeden Zug und zum Ende einen Eintrag enthält. Jeder Eintrag ist ein Tuple aus 4 Werten.
    """
    def __init__(self, player1, player2, printMoves = False):
        self.__playerCallback = (player1, player2)
        self.__playerName = (player1.__name__ + " (1)", player2.__name__ + " (2)")
        self._printMoves = printMoves
        self.__nextPlayer = 1
        self.__nextMove = 0
        self.__moveRecords = []

    def setPrintMoves(self, printMoves):
        """Setzt den Wert von _printMoves, der angibt ob die jeweiligen Züge direkt mit print() ausgeschrieben werden sollen oder nicht."""
        self._printMoves = printMoves

    @property
    def nextPlayer(self):
        """Gibt den Spieler (1 oder 2) zurück, dessen Zug gerade kommt. Wenn das Spiel schon beendet wurde, ist der Wert 0 (unentschieden), -1 oder -2."""
        return self.__nextPlayer

    @property
    def nextMove(self):
        """Gibt zurück, wievielter Zug gerade kommt, oder bei Spielende die Anzahl insgesamt gemachter Züge."""
        return self.__nextMove

    @property
    def gamePanel(self):
        """Das konkrete Spiel gibt das Spielfeld in seinem Rohmodell zurück, damit die Spieler-Callbacks daraus den Spielstand vollständig erkunden können.
        Warnung: Bei Listen oder noch komplexeren Strukturen muss eine Kopie zurückgegeben, damit der Spielstand von aussen unveränderbar bleibt!
        """
        return None

    def play(self):
        """Startet das Spiel und ruft alternierend beide Spieler-Strategien auf, bis eine gewinnt oder das Spiel mit unentschieden endet.
        Die Züge werden in einer Schleife abgearbeitet, solange es kein Gewinner (oder unentschiedenes Spielende) gibt:
        1. __nextMove wird um 1 erhöht und der __playerCallback vom __nextPlayer wird aufgerufen. Dieser Antwortet mit einem 'move'.
        2. Der 'move' wird geprüft, ob er den Regeln und dem aktuellen Stand entspricht. Falls nicht (ValueError), dann endet das Spiel mit dem Sieg des anderen Spielers.
        3. Der 'move' wird ausgeführt in _doMove(), dessen return-Wert der nächste Spieler angibt. In manchen Spielen kann ein Spieler noch ein- oder mehrmals ziehen.
        4. Es wird geprüft ob das Spiel beendet ist (_checkEnd()). Falls ja, speichern wir den Resultat ab und die Methode wird beendet, sonst kommt der nächste Zug.
        """
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
        """Das konkrete Spiel prüft, ob der gewählte Zug des aktuellen Spielers den Regeln und dem aktuellen Stand entspricht.

        Raises:
            ValueError: Im Falle eines Problems wird ein ValueError mit entsprechendem Text geworfen.
        """
        pass

    def _doMove(self, move):
        """Im konkreten Spiel wird der aktuelle Zug ausgeführt. Zurückgegeben wird der Spieler (1 oder 2) der als nächster kommt."""
        return 0

    def _checkEnd(self, move):
        """Gibt an ob das Spiel mit unentschieden beendet ist (0) oder ein Spieler gewonnen hat (1 oder 2), oder noch nicht beendet ist (None)."""
        return None

    def __recordState(self, state):
        """Speichert den Zug und den Spielstand ab um nach Spielende den Spielablauf Schritt für Schritt ansehen zu können.
        Der 'state' Argument sollte ein Tuple mit folgenden Werten beinhalten: (Zugindex, Spieler, Zug, Spielbrett nach dem Zug).

        Warnung! Beim Spielbrett, der meistens einfach das gamePanel ist, muss man aufpassen, eine später nicht mehr veränderbare Struktur einzugeben.
                 Vor allem bei List-Werten kann es vorkommen, dass - wenn der Wert direkt übergeben wurde - bei weiteren Zügen alle vorher gespeicherten
                 Spielstände die neuen Werte in der Liste übernehmen. Aus diesem Grund sollten bei List-Werten immer eine Kopie eingegeben werden!
        """
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
        """Das konkrete Spiel gibt das gamePanel als String zurück, damit es auch für Menschen einfach interpretierbar wird."""
        return firstLine + str(gamePanel)

    def getPlayerNames(self):
        """Gibt das Spiel und den Namen der gegeneinander antretenden Spieler/Strategien zurück."""
        return "{} Spiel: {} gegen {}".format(type(self).__name__, self.__playerName[0], self.__playerName[1])

    def _getLastStatesForNextPlayer(self):
        """Gibt die letzten Spielstände zurück seit dem letzten Zug des aktuellen __nextPlayer Spielers."""
        lastStates = []
        for state in self.__moveRecords[::-1]:
            lastStates.insert(0, state) # Wir fügen immer am Anfang der Liste ein, damit die Reihenfolge gut wird
            if state[1] == self.__nextPlayer:
                return lastStates
        return lastStates

    def _getState(self, index):
        """Gibt den Spielstand als 4-er Tuple (Zugindex, Spieler, Zug, Spielbrett nach dem Zug) nach dem gewählten Zug zurück."""
        return self.__moveRecords[index % len(self.__moveRecords)]

    def getStateString(self, index):
        """Gibt den Spielstand als String nach dem gewählten Zug zurück."""
        return self.stateToString(self._getState(index))

# -------------------- Human player callback --------------------   
def human(game):
    """Ein Callback für einen menschlichen Spieler, der den Benutzer um ihren Zug fragt.
    Dieser Callback darf in jedem Spiel generell verwendet werden, weil er den gewählten Zug zuerst mit game.checkMove() überprüft.
    """
    move = None
    exc = ""
    for state in game._getLastStatesForNextPlayer():
        print(game.stateToString(state) + "\n")
    while move is None:
        try:
            move = eval(str(input(exc + str(game.nextMove) + ". Zug kommt, was ziehst du? ")))
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

def playOne(createGame, player1, player2, printMoves = False):
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
