# Standard Imports
import time

# 3rd Party Imports
import pyautogui as pg
import numpy as np

#from main import *
from board import Board



time.sleep(3)
board = Board((16,16), 40)

window = board.find_window()

board.test_click()



# 10 moves
for n in range(15):

    # Read board and construct probability distribution
    board.read_board(window)
    probas = board.get_probas()

    click_lows = True
    mark_bombs = True

    # Get low probabilities
    try:
        low = probas[(probas > 0) & (probas < 0.3)].min()
        lows = np.where(probas == low)
    except:
        click_lows = False

    # Get high probabilities
    try:
        highs = np.where(probas >= 1.3)
    except:
        mark_bombs = False


    if click_lows:
        # Click the lowest probability tile(s)
        for row, col in zip(lows[0], lows[1]):
            board.click_tile(row, col)

    if mark_bombs:
        # Mark bombs
        for row, col in zip(highs[0], highs[1]):

            # If it's already marked, don't mark it again
            if (row, col) in board.bombs:
                continue

            board.mark_bomb(row, col)

    # If now low or high probabilites, click randomly
    if not (click_lows or mark_bombs):
        row = np.random.randnint(0,16)
        col = np.random.randnint(0,16)

        if (row,col) in board.bombs:
            continue
        else:
            board.click(row, col)
















