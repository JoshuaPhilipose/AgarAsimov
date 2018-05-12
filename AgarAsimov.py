import webbrowser
import time
import pyautogui
from pyautogui import typewrite
import random
import numpy
from PIL import Image
from PIL import ImageGrab

#TODO: Come up with a better organizatioal structure, right now the newest portions just go at the bottom

mouseSpeed = .4
center = (1080, 760)
topBuffer = 140
backgroundTileColor = (242, 251, 255)

# Loading the Game
def loadGame():
    url = 'http:www.agar.io'
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url)
    for i in range(1, 11):
        print "AI Takes Over in: " , (11 - i)
        time.sleep(1)

    #TODO: Below code caused bot to be flagged as a bot. Implement login sequence that beats Miniclip's bot-scanner.

    # Logging In; Co-ords are specific to 2160 x 1440 resolution screens with standard zoom

    # Agar detected the bot, so now I'm loading manually

    # typewrite('AgarAsimov v2.8', interval=0.25)
    # time.sleep(1)
    # x = 990
    # y = 370
    #
    # pyautogui.moveTo(x, y, mouseSpeed, pyautogui.easeInElastic)
    # pyautogui.click()
    #
    # # Load Time
    # time.sleep(1)

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

def crossMeasure(x, y, GameState):
    # Take the input dot, measure the vertical and horizontal distance, return the max size.
    maxX = 0
    maxY = 0
    color = GameState.getpixel((x + 10, y + 10))

    # Measuring X & Y length of same color
    for i in xrange(x, 220, -1):
        if GameState.getpixel((i, y)) == color:
            maxX += 1
        else:
            break
    for i in xrange(x, 1920, 1):
        if GameState.getpixel((i, y)) == color:
            maxX += 1
        else:
            break
    for j in xrange(y, 360, -1):
        if GameState.getpixel((x, j)) == color:
            maxY += 1
        else:
            break
    for j in xrange(y, 1220, 1):
        if GameState.getpixel((x, j)) == color:
            maxY += 1
        else:
            break

    #Handling edge case in case the coordinate of a line is inputted
    if (maxX > 20 and maxY > 20):
        return (maxX, maxY)
    else:
        return 0

def letsPlay():
    # TODO: So this scans the screen in a smaller range around the bot, and returns the coords/measurement of
    #       the non-background particles.
    #       1) Need to skip a certain scan length to avoid re-measuring/scanning the same unit many times
    #       2) Need to ensure measurement size is accurate
    #       3) Need to find a way to distinguuish dots from viruses.
    #       4) Need to actually implement the AI lol

    time.clock()
    GameState = pyautogui.screenshot('GameState.png')
    z = 0
    for x in xrange(220, 1920, 15):
        for y in xrange(360, 1220, 15):
            color = GameState.getpixel((x, y))
            if color != backgroundTileColor:
                measure = crossMeasure(x, y, GameState)
                if measure != 0:
                    # x += measure[0]
                    # y += measure[1]
                    # if
                    print "X, Y, measure: ", x, " ", y, " ", measure
                    z += 1
            #print color
    print("TOTAL NUMBER of UNITS FOUND:")
    print z
    print time.clock()



if __name__ == '__main__':
    loadGame()
    letsPlay()
    #sampleMovement()
