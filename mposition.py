import pyautogui, sys


print('X and Y coords of mouse for pyautogui use; 0,0 is top right.')
try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print positionStr + '\r',
        sys.stdout.flush()
except KeyboardInterrupt:
    print '\n'
