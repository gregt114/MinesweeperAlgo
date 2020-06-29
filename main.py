# Standard Imports
import time

# 3rd Party Imports
import pyautogui as pg
import numpy as np

# Local Imports
from board import Board

dim_x = 16
dim_y = 16


def test_click():
    unchecked_coords_gen = pg.locateAllOnScreen("images/hidden.png", confidence=0.9)
    coords = next(unchecked_coords_gen)
    pg.click(coords)


def read_board(area):
    hiddens = list(pg.locateAllOnScreen("images/hidden.png", region=area, confidence=0.95))
    clears = list(pg.locateAllOnScreen("images/clear.png", region=area, confidence=0.95))     
    ones = list(pg.locateAllOnScreen("images/one.png", region=area, confidence=0.95))
    twos = list(pg.locateAllOnScreen("images/two.png", region=area, confidence=0.95))
    threes = list(pg.locateAllOnScreen("images/three.png", region=area, confidence=0.95))

    return hiddens, clears, ones, twos, threes


def find_window():
    """
    Returns left, top, width, height of window
    """
    window = pg.locateOnScreen("images/blank_board.png", confidence=0.95)
    
    return (window.left, window.top, window.width, window.height)




time.sleep(3)

window = find_window()

test_click()

time.sleep(0.5)

hs, cs, ones, twos, threes = read_board(window)

        
# Add labels to Box objects
board_data = []
for lst,name in zip([hs, cs, ones, twos, threes], ["h","c","1","2","3"]):
    for tile in lst:
        board_data.append([pg.center(tile), name])



#print(board_data[50:])




board_sorted = sorted(board_data, key=lambda x: (x[0].y,x[0].x))

final = np.empty(dim_x*dim_y,dtype=str)
for i in range(len(final)):
    final[i] = board_sorted[i][1]
    
final = final.reshape(dim_x, dim_y)

print(final)


# clear tiles are RGB (240,239, 238)
# hidden tiles are RGB(red=186, green=189, blue=182)
