import webbrowser
import time
import pyautogui
from pyautogui import typewrite
import random

# Loading the Game
url = 'http:www.agar.io'
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
webbrowser.get(chrome_path).open(url)
time.sleep(7)

# Logging In; Co-ords are specific to 2160 x 1440 resolution screens with standard zoom
typewrite('AgarAsimov')
time.sleep(random.randint(1, 3))
x = 990
y = 370
pyautogui.click(x = x, y = y)
