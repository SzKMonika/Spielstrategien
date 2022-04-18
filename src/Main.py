import random
from Game import Game
from NimGame import Nim
from NimMultiGame import NimMulti
from Kalaha import Kalaha
from VierGewinnt import VierGewinnt
from Mastermind2 import Mastermind, MastermindStrategy

nim = lambda p1, p2: Nim(p1, p2, 15, 3, True)
nimMulti = lambda p1, p2: NimMulti(p1, p2, [1, 3, 5, 7], True)
kalaha = lambda p1, p2: Kalaha(p1, p2)
vierGewinnt = lambda p1, p2: VierGewinnt(p1, p2)
mastermind = lambda p1, p2: Mastermind(p1, p2)

# -------------------- STRATEGIE --------------------   

def Nim_meineStrategie(game):
    if game.gamePanel <= game.maxTake + 1:
        nextTake = game.gamePanel - 1
    else:
        nextTake = random.randint(1, game.maxTake)
    return (nextTake if nextTake > 0 else 1)

# -------------------- MAIN --------------------   

#Game.playOne(nim, Nim.level2, Game.human)
#Game.playOne(nimMulti, NimMulti.level2, NimMulti.level3)
#Game.playOne(kalaha, Kalaha.level2p(3), Game.human)
#Game.playOne(vierGewinnt, Game.human, VierGewinnt.level4)
#Game.playOne(mastermind, mmstrategy.level3, Game.human)

Game.playMany(nim, Nim.level2, Nim_meineStrategie, 100)
#Game.playMany(nimMulti, NimMulti.level2, NimMulti.level3, 100)
#Game.playMany(kalaha, Kalaha.level2p(3), Kalaha.level1, 100)
#Game.playMany(vierGewinnt, VierGewinnt.level2, VierGewinnt.level3, 100)
#Game.playMany(mastermind, Mastermind.level3p(), Mastermind.level2, 100)