import inspect, random, sys
from games.game import Game
from games.nim import Nim
from games.nim_multi import NimMulti
from games.kalaha import Kalaha
from games.vier_gewinnt import VierGewinnt
from games.mastermind2 import Mastermind, MastermindStrategy
import strategy

def listFunctions(module, prefix = ""):
    functions = []
    for name in dir(module):
        obj = getattr(module, name)
        if inspect.isfunction(obj) and obj.__name__.startswith(prefix):
            functions.append(module.__name__ + "." + obj.__name__)
    return functions

def nim(p1, p2):
    return Nim(p1, p2, 15, 3, False)

def nimMisere(p1, p2):
    return Nim(p1, p2, 15, 3, True)

def nimMulti(p1, p2):
    return NimMulti(p1, p2, [1, 3, 5, 7], False)

def nimMultiMisere(p1, p2):
    return NimMulti(p1, p2, [1, 3, 5, 7], True)

def kalaha(p1, p2):
    return Kalaha(p1, p2)

def vierGewinnt(p1, p2):
    return VierGewinnt(p1, p2)

def mastermind(p1, p2):
    return Mastermind(p1, p2)

# -------------------- MAIN --------------------
if __name__ == "__main__":
    gamesDict = { 1: "nim", 2: "nimMisere", 3: "nimMulti", 4: "nimMultiMisere", 5: "kalaha", 6: "vierGewinnt", 7: "mastermind" }
    classesDict = { 1: Nim, 2: Nim, 3: NimMulti, 4: NimMulti, 5: Kalaha, 6: VierGewinnt, 7: Mastermind }

    game = int(input("Bitte wähle den Spiel aus " + str(gamesDict) + ": "))

    strategies = listFunctions(classesDict[game] , "level") + listFunctions(strategy) + ["Game.human"]
    strategiesDict = { i + 1 : strategies[i] for i in range(len(strategies)) }

    player1 = int(input("Bitte gib die Strategie des 1. Spielers an " + str(strategiesDict) + ": "))
    player2 = int(input("Bitte gib die Strategie des 2. Spielers an " + str(strategiesDict) + ": "))
    count = int(input("Bitte gib die Anzahl Durchführungen an: "))

    if count <= 1:
        Game.playOne(eval(gamesDict[game]), eval(strategiesDict[player1]), eval(strategiesDict[player2]))
    else:
        Game.playMany(eval(gamesDict[game]), eval(strategiesDict[player1]), eval(strategiesDict[player2]), count)

#Game.playOne(nim, Nim.level2, Game.human)
#Game.playOne(nimMulti, NimMulti.level2, NimMulti.level3)
#Game.playOne(kalaha, Kalaha.level2p(3), Game.human)
#Game.playOne(vierGewinnt, Game.human, VierGewinnt.level4)
#Game.playOne(mastermind, mmstrategy.level3, Game.human)

#Game.playMany(nim, Nim.level2, Nim_meineStrategie, 100)
#Game.playMany(nimMulti, NimMulti.level2, NimMulti.level3, 100)
#Game.playMany(kalaha, Kalaha.level2p(3), Kalaha.level1, 100)
#Game.playMany(vierGewinnt, VierGewinnt.level2, VierGewinnt.level3, 100)
#Game.playMany(mastermind, Mastermind.level3p(), Mastermind.level2, 100)