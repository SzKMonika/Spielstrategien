"""Dieses Modul beinhaltet alle eigenen Strategien, die für die Spiele von main.py genutzt werden können.
Diese sind jeweils eine Funktion mit einem Argument (game) und deren Name muss abhängig vom Spiel mit
'nim_', 'nimMulti_', 'kalaha_', 'vierGewinnt_' oder 'mastermind_' anfangen.
"""
import random

# -------------------- Eigene Strategien --------------------
def nim_beispielStrategie(game):
    """Eine einfache Beispiel-Strategie für Nim (Standard)."""
    if game.gamePanel <= game.maxTake + 1:
        nextTake = game.gamePanel - 1
    else:
        nextTake = random.randint(1, game.maxTake)
    return (nextTake if nextTake > 0 else 1)
