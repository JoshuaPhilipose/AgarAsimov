import webbrowser
import time
import pyautogui
from pyautogui import typewrite
import random
import numpy
from PIL import Image
from PIL import ImageGrab

#TODO: Come up with a better organizational structure, right now the newest portions just go at the bottom

mouseSpeed = .4
center = (1080, 760)
topBound = 140
leftBound = 0
rightBound = 2160
bottomBound = 1380
backgroundTileColor = (242, 251, 255)
alive = False

# Loading the Game
def loadGame():
    url = 'http:www.agar.io'
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url)
    for i in range(1, 16):
        print "AI Takes Over in: " , (16 - i)
        time.sleep(1)
    global alive
    alive = True

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
    #We just set r = 300 because we want that to be the radius, don't care what it actually is
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
        y = random.randint(1, 1440) + topBuffer
        translateAndMove(x, y)
        time.sleep(1)

def flee(x, y):
    # Flees in the direction opposite the given coordinate
    tup = pyToRegCoords(x, y)
    newTup = (-tup[0], -tup[1])
    newestTup = regToPyCoords(newTup[0], newTup[1])
    translateAndMove(newestTup[0], newestTup[1])

def crossMeasure(x, y, GameState, gap):
    # Take the input dot, measure the vertical and horizontal distance, return the max size.
    maxX = 0
    maxY = 0
    try:
        color = GameState.getpixel((x + 10, y + 10))
    except KeyboardInterrupt:
        print '\n'
    except:
        color = GameState.getpixel((x, y))

    # Measuring X & Y length of same color
    for i in xrange(x, leftBound, -1 * gap):
        if GameState.getpixel((i, y)) == color:
            maxX += gap
        else:
            break
    for i in xrange(x, rightBound, gap):
        if GameState.getpixel((i, y)) == color:
            maxX += gap
        else:
            break
    for j in xrange(y, topBound, -1 * gap):
        if GameState.getpixel((x, j)) == color:
            maxY += gap
        else:
            break
    for j in xrange(y, bottomBound, gap):
        if GameState.getpixel((x, j)) == color:
            maxY += gap
        else:
            break

    #Handling edge case in case the coordinate of a line is inputted
    if (maxX > 20 and maxY > 20):
        return (maxX, maxY, max(maxX, maxY))
    else:
        return 0

def letsPlay():
    # TODO: So this scans the screen in a smaller range around the bot, and plays based off that.
    #
    #       1) Need to initialize skipping self
    #       2) Need to ensure measurement size is accurate
    #       3) Need to find a way to distinguish dots from viruses.
    #       4) Need to actually implement the AI lol

    # TODO: The AI is essentially solving this problem:
    #           Given the input gamestate (144 x 96 matrix), which output direction should the agent go in to maximize our score?
    #       Training Data should be stored in separate file to allow for multi-session memory
    #       3 Possible outputs are mouse movement, splitting, and shooting out a blob
    #       Can store smaller blobs rewards as measurement size, store larger ones as negative size
    #       First priority is staying alive, second is growing larger - utilize living reward to disincentivize hiding 24/7

    totalTimeAlive = time.time()
    hostileMap = numpy.zeros((9, 9))

    global alive
    while alive:
        # Initializing
        startTime = time.time()

        z = 0
        # map = {}
        sizeThreshhold = 70
        skipRanges = [(1806, 2142, 152, 567)] # Initialized with the coordinates of the leaderboard
        prevColor = backgroundTileColor

        GameState = pyautogui.screenshot('GameState.png')
        gameOverColor = (255, 255, 255)
        if GameState.getpixel((1080, 222)) == gameOverColor:
            alive = False
            print "hostileMap at death: ", hostileMap
            print "TOTAL TIME ALIVE: ", time.time() - totalTimeAlive, " seconds."
            break
        hostileMap = numpy.zeros((9, 9))

        # TODO: just make a 9x9 grid of "feelers" then use value iteration to decide between up, down, left, right
        for x in xrange(9):
            for y in xrange(9):
                xCoord = 360 + x * 180
                yCoord = 240 + y * 120
                color = GameState.getpixel((xCoord, yCoord))
                if color != backgroundTileColor and color != prevColor:
                    measure = crossMeasure(xCoord, yCoord, GameState, 10)
                    if measure > sizeThreshhold:
                        hostileMap[x, y] = measure[2]
                        flee(xCoord, yCoord)
        hostileMap = numpy.zeros((9, 9))

        # TODO: What we need is a series of maps. Closest one has high density, but short around the agent.
        #       mid range is mid, entire screen has very wide sweep. calculate an optimal policy for each,
        #       then calculate final policy based off weights.

        # skipRange.append((360, 1800, 240, 1200))
        # for x in xrange(leftBound, rightBound, 360):
        #     for y in xrange(topBound, bottomBound, 240):
        #         for skipRange in skipRanges:
        #             if (x > skipRange[0] and x < skipRange[1]):
        #                 if (y > skipRange[2] and y < skipRange[3]):
        #                     y = min(skipRange[3], bottomBound)
        #
        # del skipRange[1]
        # For smaller window use 220 to 1920, bigger use 0 to 2160

        # for x in xrange(leftBound, rightBound, 15):
        #     # For smaller window use 360 to 1220, bigger use topBound to bottomBound
        #     for y in xrange(topBound, bottomBound, 15):
        #         # Skipping ranges where we already know something is there
        #         # TODO: This skips rectangular ranges, but the units found are circular
        #         for skipRange in skipRanges:
        #             if (x > skipRange[0] and x < skipRange[1]):
        #                 if (y > skipRange[2] and y < skipRange[3]):
        #                     y = min(skipRange[3], bottomBound)
        #
        #         # Identifying and measuring units
        #         color = GameState.getpixel((x, y))
        #         if color != backgroundTileColor and color != prevColor:
        #             measure = crossMeasure(x, y, GameState, 2)
        #             if measure != 0:
        #                 # Appends another range of values to skip over
        #                 skipRanges.append((x, x + measure[2], y - measure[2], y + measure[2] / 2))
        #                 if (measure < 400): #TODO: Change this 40 to agent's size / 1.3
        #                     map[measure[2]] = measure[2](x, y)
        #                 else:
        #                     map[(x, y)] = -1 * measure[2]
        #
        #                 # print "X, Y, measure: ", x, " ", y, " ", measure, color
        #                 z += 1
        #         prevColor = color
        #
        # # This is just brute force, doesn't discount future rewards - change!
        # optimalDirection = max(map, key=map.get)
        # translateAndMove(optimalDirection[0], optimalDirection[1])

        # Key Performance Indicators
        # print("TOTAL NUMBER of UNITS FOUND:")
        # print z
        endTime = time.time()
        print "Loop took ", endTime - startTime, " seconds."
        # END OF WHILE LOOP
# END OF letsPlay()

    # Testing for accurate unit detection
    # Amazing test, just pulled up a fullscreen version of the gamestate and had it identify units
    # time.sleep(10)
    # for s in skipRanges:
    #     pyautogui.moveTo(s[0], (s[2] +  s[3]) / 2, .2)
    #     time.sleep(1)



if __name__ == '__main__':
    loadGame()
    letsPlay()
    #sampleMovement()
