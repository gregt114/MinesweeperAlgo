# Standard Imports
import time

# 3rd Party Imports
import pyautogui as pg


from main import test_click, read_board, dim_x, dim_y

















"""
def get_clear_hidden():
    current_coords = list(pg.locateCenterOnScreen("images/clear.png", confidence=0.95))
    x0, y0 = int(current_coords[0]),int(current_coords[1])

    ret = []


    for j in range(dim_y):
        for i in range(dim_x):
            x,y = int(current_coords[0]), int(current_coords[1])

            if pg.pixelMatchesColor(x, y, (222,222,220), tolerance=3):
                ret.append([x,y,"c"])
            elif pg.pixelMatchesColor(x, y, (186,189,182), tolerance=3):
                ret.append([x,y,"h"])
            current_coords = [x0+30*i, y0+30*j]

    return ret
"""