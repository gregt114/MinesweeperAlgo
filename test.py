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

print()

probas = get_proba(board)
print(probas)

print()

print(window[0], window[1])

for i in range(len(probas)):
    for j in range(len(probas[0])):
        if probas[i][j] > 1:
            pg.moveTo(window[0] + 17*j, window[1] + 17*i,1)



















