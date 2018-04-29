import webbrowser
import time
import pyautogui
from pyautogui import typewrite
import random
import numpy
from PIL import Image
from PIL import ImageGrab

mouseSpeed = .2
center = (1080, 760)
topBuffer = 140
# Loading the Game
def loadGame():
    url = 'http:www.agar.io'
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url)
    time.sleep(3)

    # Logging In; Co-ords are specific to 2160 x 1440 resolution screens with standard zoom
    typewrite('AgarAsimov v2.8', interval=0.25) # Google Chrome remembers my username from last session
    time.sleep(1)
    x = 990
    y = 370

    pyautogui.moveTo(x, y, mouseSpeed, pyautogui.easeOutQuad)
    pyautogui.click()

    # Now we need to actually play!
    time.sleep(.2)

    GameState = pyautogui.screenshot('GameState.png')

def translateAndMove(x, y):
    #Takes raw pyautogui coords and moves mouse to the appropriate location in a 300 px radius of the center of the game

    #First step: translating from pyautogui coordinates to regular coords with 0 at the center
    tup = pyToRegCoords(x, y)
    x = tup[0]
    y = tup[1]

    #Second step: translating to unit polar coordinates with r = 300 px
    r = 300
    angle = numpy.arctan2(y, x)

    #Third step: translating back to regular coordinates
    x = r * numpy.cos(angle)
    y = r * numpy.sin(angle)

    #Fourth step: translating back to pyautogui coordinates and moving
    tup = regToPyCoords(x, y)
    pyautogui.moveTo(tup[0], tup[1], mouseSpeed, pyautogui.easeOutQuad)

def pyToRegCoords(x, y):
    x = x - 1080
    y = y - 758
    return (x, y)

def regToPyCoords(x, y):
    #translates to pyautogui coords: (0,0) at top left corner
    x = x + 1080
    y = y + 758
    return (x, y)

def sampleMovement():
    for i in range(5):
        x = random.randint(1, 2160)
        y = random.randint(1, 1440) + 170
        translateAndMove(x, y)
        time.sleep(1)

def flee(x, y):
    # Flees in the direction opposite the given coordinate
    tup = pyToRegCoords(x, y)
    tup[0] = -tup[0]
    tup[1] = -tup[1]
    tup = regToPyCoords(tup[0], tup[1])
    translateAndMove(tup[0], tup[1])

def crossMeasure(x, y):
    # Take the input dot, measure the vertical and horizontal distance, return the max size.
    x = x + 1
    y = y + 1

def letsPlay():
    time.clock()
    GameState = pyautogui.screenshot('GameState.png')
    x = 0
    for x in range(220, 1920, 15):
        for y in range(360, 1220, 15):
            color = GameState.getpixel((x, y))
            x += 1
            # print color
    print("TOTAL NUMBER:")
    print x
    print time.clock()



if __name__ == '__main__':
    #loadGame()
    letsPlay()
    #sampleMovement()
