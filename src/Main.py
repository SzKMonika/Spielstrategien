import inspect, random, sys
from Game import Game
from NimGame import Nim
from NimMultiGame import NimMulti
from Kalaha import Kalaha
from VierGewinnt import VierGewinnt
from Mastermind2 import Mastermind, MastermindStrategy

def listFunctions(numParams):
    # TODO Die Strategien sollen möglicherweise in einer anderen Datei kommen und dann kann man die einfach(er) referenzieren.
    # Die hiesige games sollen manuell in eine Liste/Dictionary geladen werden und das hier sollte nur für die Strategien verwendet werden.
    me = __import__(inspect.getmodulename(__file__)) # TODO <--Möglicherweise deswegen wird das Module zweimal ausgeführt!
    functions = []
    for name in dir(me):
        obj = getattr(me, name)
        if inspect.isfunction(obj) and obj.__name__ != 'listFunctions':
            if (len(inspect.signature(obj).parameters)) == numParams: # TODO <--Funktioniert nicht in Tigerjython!
                functions.append(obj.__name__)
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

# -------------------- Eigene Strategien --------------------   

def Nim_meineStrategie(game):
    if game.gamePanel <= game.maxTake + 1:
        nextTake = game.gamePanel - 1
    else:
        nextTake = random.randint(1, game.maxTake)
    return (nextTake if nextTake > 0 else 1)

# -------------------- MAIN --------------------
strategies = listFunctions(1)
games = listFunctions(2)
strategiesDict = { i + 1 : strategies[i] for i in range(len(strategies)) }
gamesDict = { i + 1 : games[i] for i in range(len(games)) }

game = int(input("Bitte wähle den Spiel aus " + str(gamesDict) + ": "))
player1 = str(input("Bitte gib die Strategie des 1. Spielers an: "))
player2 = str(input("Bitte gib die Strategie des 2. Spielers an: "))
count = int(input("Bitte gib die Anzahl Durchführungen an: "))

if count <= 1:
    Game.playOne(eval(gamesDict[game]), eval(player1), eval(player2))
else:
    Game.playMany(eval(gamesDict[game]), eval(player1), eval(player2), count)

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