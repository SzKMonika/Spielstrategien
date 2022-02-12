import os
import sys
from time import sleep

from VierGewinnt import *

IS_PYTHON3 = sys.version_info[0] > 2

IS_JYTHON = sys.executable.endswith("jython.exe") or sys.platform.startswith("java")

if IS_JYTHON:
    #from gpanel import *
    from gconsole import *
    makeConsole()
    println = gprintln
    waitForKey = getKeyCodeWait
    clr = clear
else:
    import builtins
    import keyboard # https://stackoverflow.com/questions/24072790/how-to-detect-key-presses
    println = builtins.print
    waitForKey = keyboard.read_key
    clr = (lambda: os.system('clear')) if os.name == 'posix' else (lambda: os.system('cls')) # https://www.scaler.com/topics/how-to-clear-screen-in-python/

mygame = VierGewinnt(VierGewinnt_L4, VierGewinnt_L4, "L4", "L4")
mygame.play()

keyPressed = waitForKey()
index = 0
while keyPressed != 'q' and keyPressed != 113:
    clr()
    println(mygame.getPlayerNames())
    println('')
    println(mygame.getState(index))
    sleep(0.2)
    keyPressed = waitForKey()
    if keyPressed == 37 or keyPressed == 'nach-links':
        index -= 1
    if keyPressed == 39 or keyPressed == 'nach-rechts':
        index += 1
    if keyPressed == 40 or keyPressed == 'nach-unten':
        index = 0
