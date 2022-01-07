from NimGame import *

def meineStrategie(game):
    if game.sticks <= game.maxTake + 1:
        nextTake = game.sticks - 1
    else:
        nextTake = random.randint(game.minTake, game.maxTake)
    return (nextTake if nextTake > 0 else 1)

# -------------------- MAIN --------------------   
for i in range(5):
    nimGame = NimGame(meineStrategie, computer2, 15, 3)
    nimGame.play()
    nimGame.printAllStates()
