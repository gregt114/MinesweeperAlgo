# Standard Imports
import time

# 3rd Party Imports
import pyautogui as pg


from main import *




time.sleep(3)

window = find_window()





test_click(window)

time.sleep(2)

board = get_board(window)
print(board)
print()


proba = get_proba(board)
print(proba)

# hiddens = list(pg.locateAllOnScreen("images/hidden.png", region=window, confidence=0.95))
# print(hiddens[0])


for i in range(len(proba)):
    for j in range(len(proba[0])):
        if proba[i][j] > 0:
            pg.moveTo(window[0] + 17*j + 8, window[1] + 17*i + 8, 0.5)
            pg.click(button="right", clicks=2)













