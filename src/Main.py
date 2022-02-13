import random
from Game import *
from NimGame import *
#from NimMultiGame import *
#from Kalaha import *
#from VierGewinnt import *

def Nim_meineStrategie(game):
    if game.gamePanel <= game.maxTake + 1:
        nextTake = game.gamePanel - 1
    else:
        nextTake = random.randint(game.minTake, game.maxTake)
    return (nextTake if nextTake > 0 else 1)

# -------------------- MAIN --------------------   
myGame = NimGame(Nim_meineStrategie, Nim_L1, 15, "Meine Strategie")
#myGame = NimMultiGame(Game.human, NimMulti_L2, [1,3,5,7])
#myGame = Kalaha(Kalaha_L2, Kalaha_L2, "L2", "L2")
#myGame = VierGewinnt(VierGewinnt_L4, VierGewinnt_L4, "L4", "L4")

playOnce(myGame)
