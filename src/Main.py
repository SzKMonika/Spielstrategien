import random
from Game import *
from NimGame import *
from NimMultiGame import *
from Kalaha import *
from VierGewinnt import *

nim = lambda p1, p2: NimGame(p1, p2, 15, 3, True)
nimMulti = lambda p1, p2: NimMultiGame(p1, p2, [1, 3, 5, 7], True)
kalaha = lambda p1, p2: Kalaha(p1, p2)
vierGewinnt = lambda p1, p2: VierGewinnt(p1, p2)

# -------------------- STRATEGIE --------------------   

def Nim_meineStrategie(game):
    if game.gamePanel <= game.maxTake + 1:
        nextTake = game.gamePanel - 1
    else:
        nextTake = random.randint(1, game.maxTake)
    return (nextTake if nextTake > 0 else 1)

# -------------------- MAIN --------------------   

playOne(nim, Nim_L1, human)
#playOne(nimMulti, NimMulti_L2, NimMulti_L3)
#playOne(kalaha, Kalaha_L2p(3), human)
#playOne(vierGewinnt, human, VierGewinnt_L4)

#playMany(nim, Nim_L2, Nim_meineStrategie, 200)
#playMany(nimMulti, NimMulti_L2, NimMulti_L3, 100)
#playMany(kalaha, Kalaha_L2p(3), Kalaha_L3, 100)
#playMany(vierGewinnt, VierGewinnt_L2, VierGewinnt_L3, 100)