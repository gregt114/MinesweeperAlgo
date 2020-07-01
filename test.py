# Standard Imports
import time

# 3rd Party Imports
import pyautogui as pg


from main import *




time.sleep(3)

window = find_window()

test_click()

time.sleep(2)

board = get_board(window)

print(board)

print(get_neigh(board,2,0))




















