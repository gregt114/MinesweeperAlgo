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



# Game loop
while True:

    # Read board and construct score distribution
    board.read_board(window)

    board.take_turn()

    if len(board.bombs) == 40:
        break















