"""Dieses Modul beinhaltet alle eigenen Strategien, die für die Spiele von main.py genutzt werden können.
Diese sind jeweils eine Funktion mit einem Argument (game) und deren Name muss abhängig vom Spiel mit
'nim_', 'nimMulti_', 'kalaha_', 'vierGewinnt_' oder 'mastermind_' anfangen.

In allen Strategien können die Properties von game, und bei VierGewinnt die Hilfsmethoden verwendet werden:
game.gamePanel: Gibt in allen Spielen das Modell des Spielfeldes zurück.
game.nextPlayer: Gibt in allen Spielen den Spieler (1 oder 2) zurück, dessen Zug gerade kommt.
game.nextMove: Gibt in allen Spielen zurück, wievielter Zug gerade kommt.

Weitere Details (Modell, Properties, Hilfsmethoden) pro Spiel
-------------------------------------------------------------
Nim:
- game.gamePanel ist einfach eine int-Zahl mit der Anzahl verbleibenden Objekten.
- game.maxTake: Maximale Anzahl der Objekte, die in einem Zug weggenommen werden können, also 3.
- game.lastOneLoses: Gibt an, welche Variante gespielt wird: False = Standard-Variante, True = Misère-Variante.

NimMulti:
- game.gamePanel ist eine Liste von int-Zahlen, die jeweils die Anzahl verbleibender Objekte einer Reihe angeben.
- game.lastOneLoses: Gibt an, welche Variante gespielt wird: False = Standard-Variante, True = Misère-Variante.

Kalaha:
- game.gamePanel ist eine Tuple mit 2 Listen (für die zwei Muldenreihen) mit jeweils 7 ganzen Zahlen.
                 Beide Listen haben auf Index 0 die Anzahl Steine in der Gewinnmulde, und unter Index 1 bis 6
                 befinden sich die Anzahl Steine in den Spielmulden, und zwar immer von der Gewinnmulde gezählt.
- game.getPitListForNextPlayer(): Gibt den Inhalt der Muldenreihe des aktuellen Spielers als eine Liste von Zahlen zurück.
- game.getPitListForOtherPlayer(): Gibt den Inhalt der Muldenreihe des anderen Spielers als eine Liste von Zahlen zurück.

VierGewinnt:
- game.gamePanel ist eine zweidimensionale Liste von ganzen Zahlen, die jeweils den Wert
                 0 (leeres Feld), 1 (Feld belegt von Spieler 1) oder -1 (Feld belegt von Spieler 2) haben.
- game.getColumn(int): Gibt den Inhalt der gewählten Spalte (1 bis 7) als eine Liste zurück.
- game.getRow(int): Gibt den Inhalt der gewählten Reihe (1 bis 6) als eine Liste zurück.
- game.getTokenForNextPlayer(): Gibt den Wert des Tokens als ganze Zahl (1 oder -1) für nextPlayer zurück.
- game.getDiagonalUpRight(row, column): Gibt den Inhalt der diagonalen Linie (von unten links nach oben rechts)
                                        zurück, die durch das angegebene Feld durchläuft.
- game.getDiagonalUpLeft(row, column): Gibt den Inhalt der diagonalen Linie (von unten rechts nach oben links)
                                       zurück, die durch das angegebene Feld durchläuft.
- VierGewinnt.countTokensIn(line): Gibt an, wie viele Spielsteine insgesamt in der angegebenen Linie vorkommen.

Mastermind:
- game.gamePanel ist die Liste der Züge, die jeweils aus 3-er Tuplen bestehen: (Tipp, Gut, Halbgut)
"""
import random

# -------------------- Eigene Strategien --------------------
def nim_beispielStrategie(game):
    """Eine einfache Beispiel-Strategie für Nim. Welche Variante?"""
    if game.gamePanel <= game.maxTake + 1:
        nextTake = game.gamePanel - 1
    else:
        nextTake = random.randint(1, game.maxTake)
    return (nextTake if nextTake > 0 else 1)
