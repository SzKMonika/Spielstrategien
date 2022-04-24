import random

# -------------------- Eigene Strategien --------------------
def nim_beispielStrategie(game):
    """Eine einfache Beispiel-Strategie für Nim (Standard)."""
    if game.gamePanel <= game.maxTake + 1:
        nextTake = game.gamePanel - 1
    else:
        nextTake = random.randint(1, game.maxTake)
    return (nextTake if nextTake > 0 else 1)
