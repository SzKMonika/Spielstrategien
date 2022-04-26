"""Dieses Modul ermöglicht das Starten eines beliebigen Spiels von der games-Package."""

import inspect, random, sys
import games.game
from games.nim import Nim
from games.nim_multi import NimMulti
from games.kalaha import Kalaha
from games.vier_gewinnt import VierGewinnt
from games.mastermind import Mastermind
from games.mastermind2 import Mastermind2
import strategy

def listFunctions(module, prefix = ""):
    """Diese Funktion kann für ein Modul oder Klasse (Argument module) die Namen derjenigen Methoden ausgeben, die mit dem angegebenen Prefix anfangen."""
    functions = []
    for name in dir(module):
        obj = getattr(module, name)
        if inspect.isfunction(obj) and obj.__name__.startswith(prefix):
            functions.append(module.__name__ + "." + obj.__name__)
    return functions

def nim(p1, p2):
    """Diese Funktion erstellt ein Nim-Spiel (Standard)."""
    return games.nim.Nim(p1, p2, 15, 3, False)

def nimMisere(p1, p2):
    """Diese Funktion erstellt ein Nim-Spiel (Misere)."""
    return games.nim.Nim(p1, p2, 15, 3, True)

def nimMulti(p1, p2):
    """Diese Funktion erstellt ein NimMulti-Spiel (Standard)."""
    return games.nim_multi.NimMulti(p1, p2, [1, 3, 5, 7], False)

def nimMultiMisere(p1, p2):
    """Diese Funktion erstellt ein NimMulti-Spiel (Misere)."""
    return games.nim_multi.NimMulti(p1, p2, [1, 3, 5, 7], True)

def kalaha(p1, p2):
    """Diese Funktion erstellt ein Kalaha-Spiel."""
    return games.kalaha.Kalaha(p1, p2)

def vierGewinnt(p1, p2):
    """Diese Funktion erstellt ein VierGewinnt-Spiel."""
    return games.vier_gewinnt.VierGewinnt(p1, p2)

def mastermind2(p1, p2):
    return Mastermind2(p1, p2)

def human(game):
    """Ein menschlicher Spieler, der in jedem Spiel verwendet werden kann."""
    return games.game.Game.human(game)

# -------------------- MAIN --------------------
if __name__ == "__main__":
    gamesDict = { 1: "nim", 2: "nimMisere", 3: "nimMulti", 4: "nimMultiMisere", 5: "kalaha", 6: "vierGewinnt", 7: "mastermind" }
    classesDict = { 1: Nim, 2: Nim, 3: NimMulti, 4: NimMulti, 5: Kalaha, 6: VierGewinnt, 7: Mastermind, 8: Mastermind2 }
    prefixDict = { 1: "nim_", 2: "nim_", 3: "nimMulti", 4: "nimMulti", 5: "kalaha", 6: "vierGewinnt", 7: "mastermind", 8: "mastermind" }

    game = int(input("Bitte wähle den Spiel aus " + str(gamesDict) + ": "))

    if classesDict[game] != Mastermind:
        strategies = listFunctions(classesDict[game], "level") + listFunctions(strategy, prefixDict[game]) + ["human"]
        strategiesDict = { i + 1 : strategies[i] for i in range(len(strategies)) }

        player1 = int(input("Bitte gib die Strategie des 1. Spielers an " + str(strategiesDict) + ": "))
        player2 = int(input("Bitte gib die Strategie des 2. Spielers an " + str(strategiesDict) + ": "))
        count = int(input("Bitte gib die Anzahl Durchführungen an: "))

        # Falls der Name einer Strategie-Funktion mit '_' endet, dann rufen wir sie effektiv auf, damit wir die richtige Strategie-Funktion erhalten
        strategy1 = eval(strategiesDict[player1] + ("()" if strategiesDict[player1].endswith("_") else ""))
        strategy2 = eval(strategiesDict[player2] + ("()" if strategiesDict[player2].endswith("_") else ""))
        if count <= 1:
            games.game.Game.playOne(eval(gamesDict[game]), strategy1, strategy2)
        else:
            games.game.Game.playMany(eval(gamesDict[game]), strategy1, strategy2, count)
    else: # Wir spielen Mastermind
        strategies1 = listFunctions(Mastermind, "player1") + listFunctions(strategy, prefixDict[game])
        strategies1Dict = { i + 1 : strategies1[i] for i in range(len(strategies1)) }
        strategies2 = listFunctions(Mastermind, "player2") + listFunctions(strategy, prefixDict[game]) + ["human"]
        strategies2Dict = { i + 1 : strategies2[i] for i in range(len(strategies1)) }

        player1 = int(input("Bitte gib die Strategie des 1. Spielers an " + str(strategies1Dict) + ": "))
        player2 = int(input("Bitte gib die Strategie des 2. Spielers an " + str(strategies2Dict) + ": "))
        count = int(input("Bitte gib die Anzahl Durchführungen an: "))

        # Falls der Name einer Strategie-Funktion mit '_' endet, dann rufen wir sie effektiv auf, damit wir die richtige Strategie-Funktion erhalten
        strategy1 = eval(strategies1Dict[player1] + ("()" if strategies1Dict[player1].endswith("_") else ""))
        strategy2 = eval(strategies2Dict[player2] + ("()" if strategies2Dict[player2].endswith("_") else ""))
        if count <= 1:
            game = Mastermind(strategy1, strategy2)
            game.play()
        else:
            Mastermind.playMany(strategy1, strategy2, count)
