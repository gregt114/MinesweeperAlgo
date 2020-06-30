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


def get_board(area):

    # Get locations for each type of tile
    hiddens = list(pg.locateAllOnScreen("images/hidden.png", region=area, confidence=0.95))
    clears = list(pg.locateAllOnScreen("images/clear.png", region=area, confidence=0.95))     
    ones = list(pg.locateAllOnScreen("images/one.png", region=area, confidence=0.95))
    twos = list(pg.locateAllOnScreen("images/two.png", region=area, confidence=0.95))
    threes = list(pg.locateAllOnScreen("images/three.png", region=area, confidence=0.95))

    board_data = []
    # Add labels to each type of tile (Box objects)
    # -1 is a hidden tile, 0 is clear, 1 is one, etc...
    for lst,name in zip([hiddens, clears, ones, twos, threes], [-1,0,1,2,3]):
        for tile in lst:
            board_data.append([pg.center(tile), name])

    # Sort data by positiion(first by y position, then by x for ties)
    board_sorted = sorted(board_data, key=lambda x: (x[0].y,x[0].x))

    # Create array that represents the minesweeper board and fill it
    final = np.empty(dim_x*dim_y,dtype=int)
    for i in range(len(final)):
        final[i] = board_sorted[i][1]
    
    # Reshape the 1D array into the correct matrix shape
    final = final.reshape(dim_x, dim_y)

    return final
    

    


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



print(get_board(window))
