"""Dieses Modul beinhaltet die Klasse Executor und eine umgebungsabhängige Initialiasierung, die die Funktionen
println, clr und waitForKey so aufsetzt, dass diese sowohl in TigerJython wie auch in Python (VS Code) funktionieren."""
import os, sys, time

# -------------------- class Game --------------------
class Executor():
    """Die Executor Klasse kann eine konkrete Subklasse von Game einmal oder mehrmals ausführen.

    Args:
        gameCreator: eine Funktion oder Lambda, die eine Instanz des gewählten Spiels mit den angegeben beiden Spielern erstellen kann
        player1: Eine Funktion, die die Strategie des ersten Spielers ausführt.
        player2: Eine Funktion, die die Strategie des zweiten Spielers ausführt.

    Attributes:
        _gameCreator: Der Wert vom Argument gameCreator.
        _player1: Der Wert vom Argument player1.
        _player2: Der Wert vom Argument player2.
    """
    def __init__(self, gameCreator, player1, player2):
        self._gameCreator = gameCreator
        self._player1 = player1
        self._player2 = player2

    def play(self, count):
        """Führt ein Spiel (Game) ein- oder mehrmals aus, abhängig vom Argument count."""
        if count > 1:
            self.playMany(count)
        else:
            self.playOne()

    def playOne(self, printMoves = False):
        """Führt ein Spiel (Game) einmal aus und erlaubt es nachher die Züge einzeln anzuschauen.
        
        Args:
            printMoves (bool): Gibt an, ob die Züge bzw. Spielstände auf die Konsole ausgegeben werden sollen oder nicht.
        """
        game = self._gameCreator(self._player1, self._player2)
        game.setPrintMoves(printMoves)
        game.play()
        # Das Spiel ist nun zu Ende, jetzt soll der Benutzer die Züge einzeln anschauen können.
        if IS_JYTHON:
            gconsole.makeConsole()
        println("Benutze die Pfeiltasten um jeden Spielzug einzeln anzuschauen, und q um zu beenden!")
        keyPressed = waitForKey()
        index = 0
        # Wir zeigen die Züge einzeln auf der umgebungsabhängige Konsole an, und ermöglichen vor- oder rückwärts zu gehen
        while keyPressed != 'q' and keyPressed != 81:
            clr()
            println(game.getName() + ": " + game.getPlayerNames())
            println('')
            println(game.getStateString(index))
            # Diese Verzögerung wurde wegen TigerJython eingebaut, weil sonst die Ausgabe manchmal nicht OK war
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

    def playMany(self, count = 100):
        """Führt ein Spiel (Game) mehrmals aus und gibt nachher eine Statistik aus.
        Für jedes ausgeführte Spiel gibt es fairerweise auch eine Revanche, wo die Reihenfolge der beiden Spieler getauscht wird.

        Args:
            count (int): Anzahl der Spiele die durchgespielt werden sollen. Eigentlich werden doppelt so viele Spiele ausgeführt, wegen den Revanchen. 
        """
        start = time.time()
        game1stats = [0, 0, 0]
        game1wrongmove = [0, 0, 0]
        game2stats = [0, 0, 0]
        game2wrongmove = [0, 0, 0]
        if IS_JYTHON:
            gconsole.makeConsole()

        # Wir führen das Spiel count-mal aus, aber doppelt, damit beide Spieler gleich viel anfangen können.
        for _ in range(1, count+1):
            game1 = self._gameCreator(self._player1, self._player2)
            game1.setPrintMoves(False)
            game1.play()
            # Erstes Spiel ist vorüber, wir fügen das Ergebnis der Statistik hinzu.
            winner = -game1.nextPlayer
            game1stats[winner] += 1
            if game1.isLastMoveWrong():
                game1wrongmove[winner] += 1
            # Revanche startet, aber nun sind die Spieler in umgekehrter Reihenfolge.
            game2 = self._gameCreator(self._player2, self._player1)
            game2.setPrintMoves(False)
            game2.play()
            # Im game2 sind die Spieler umgekehrt, darum arbeiten wir einfach mit negativem Gewinner bzw. Index
            winner = game2.nextPlayer
            game2stats[winner] += 1
            if game2.isLastMoveWrong():
                game2wrongmove[winner] += 1
            if IS_JYTHON:
                time.sleep(0.1)
            clr()
            out = game1.getName() + ": " + game1.getPlayerNames() + " \n"
            out += ("\n  Erster Zug    |  Unentschieden  |    Spieler (1) gewinnt     |    Spieler (2) gewinnt")
            out += ("\n    durch       |                 | (davon wegen falschem Zug) | (davon wegen falschem Zug)")
            out += ("\n----------------+-----------------+----------------------------+----------------------------")
            out += ("\n  Spieler (1)   |      {:^5}      |           {:^5}            |           {:^5}".format(game1stats[0], game1stats[1], game1stats[2]))
            out += ("\n                |                 |          ({:^5})           |          ({:^5})".format(game1wrongmove[1], game1wrongmove[2]))
            out += ("\n----------------+-----------------+----------------------------+----------------------------")
            out += ("\n  Spieler (2)   |      {:^5}      |           {:^5}            |           {:^5}".format(game2stats[0], game2stats[1], game2stats[2]))
            out += ("\n                |                 |          ({:^5})           |          ({:^5})".format(game2wrongmove[1], game2wrongmove[2]))
            out += ("\n\n(Zeit: {:5.3f} s)".format(time.time() - start))
            println(out)
        if IS_JYTHON:
            waitForKey()
            gconsole.dispose()

# -------------------- Umgebung-abhängige Initialisierung --------------------   
IS_PYTHON3 = sys.version_info[0] > 2

IS_JYTHON = sys.executable.endswith("jython.exe") or sys.platform.startswith("java")

if IS_JYTHON:
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
