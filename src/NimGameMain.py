from NimGame import *
from Game import human

def meineStrategie(game):
    if game.gamePanel <= game.maxTake + 1:
        nextTake = game.gamePanel - 1
    else:
        nextTake = random.randint(game.minTake, game.maxTake)
    return (nextTake if nextTake > 0 else 1)

# -------------------- MAIN --------------------   
for i in range(5):
    nimGame = NimGame(meineStrategie, human, 10, 3)
    nimGame.play()
