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



# 15 moves
for n in range(2):

    # Read board and construct score distribution
    board.read_board(window)
    scores = board.get_scores()
    board.reduce_board()

    print(scores)
    print(board)

    # Mark bombs
    for r in range(len(scores)):
        for c in range(len(scores[0])):
            if scores[r][c] == 100 and (r,c) not in board.bombs:
                board.mark_bomb(r,c)

    board.make_move()















