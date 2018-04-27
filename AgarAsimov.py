import webbrowser
import time
import pyautogui
from pyautogui import typewrite
import random
import numpy

# Loading the Game
url = 'http:www.agar.io'
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
webbrowser.get(chrome_path).open(url)
time.sleep(7)

# Logging In; Co-ords are specific to 2160 x 1440 resolution screens with standard zoom
typewrite('AgarAsimov v2.8', interval=0.25) # Google Chrome remembers my username from last session
time.sleep(random.randint(1, 3))
x = 990
y = 370

mouseSpeed = .2

pyautogui.moveTo(x, y, mouseSpeed, pyautogui.easeOutQuad)
pyautogui.click()

# Now we need to actually play!
time.sleep(2)
im2 = pyautogui.screenshot('my_screenshot.png')
center = (1080, 760)

#TODO: REPLACE WITH ACTUAL BRAIN

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
    # print(tup[0])
    # print(tup[1])
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

if __name__ == '__main__':
    sampleMovement()
