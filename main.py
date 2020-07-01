# Standard Imports
import time

# 3rd Party Imports
import pyautogui as pg
import numpy as np

# Local Imports
from board import Board

dim_x = 16
dim_y = 16


def test_click(area):
    unchecked_coords_gen = pg.locateAllOnScreen("images/hidden.png", region=area, confidence=0.95)
    coords = next(unchecked_coords_gen)
    pg.click(pg.center(coords))



def get_board(area):

    # Get locations for each type of tile
    hiddens = list(pg.locateAllOnScreen("images/hidden.png", region=area, confidence=0.95))
    clears = list(pg.locateAllOnScreen("images/clear.png", region=area, confidence=0.95))     
    ones = list(pg.locateAllOnScreen("images/one.png", region=area, confidence=0.95))
    twos = list(pg.locateAllOnScreen("images/two.png", region=area, confidence=0.95))
    threes = list(pg.locateAllOnScreen("images/three.png", region=area, confidence=0.95))
    fours = list(pg.locateAllOnScreen("images/four.png", region=area, confidence=0.95))
    fives = list(pg.locateAllOnScreen("images/five.png", region=area, confidence=0.95))

    board_data = []
    # Add labels to each type of tile (Box objects)
    # -1 is a clear tile, 0 is a hidden tile, 1 is one, etc...
    for lst,name in zip([clears, hiddens, ones, twos, threes, fours], [-1,0,1,2,3,4]):
        for tile in lst:
            board_data.append([tuple(pg.center(tile)), name])

    # Sort data by positiion(first by y position, then by x for ties)
    board_sorted = sorted(board_data, key=lambda x: (x[0][1],x[0][0]))

    # Create array that represents the minesweeper board and fill it
    final = np.empty(dim_x*dim_y, dtype=int)
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




def get_neigh(board,x,y):

    ylen, xlen = board.shape

    # We first need to find the corrext shape for the array
    # Corners
    if (x == 0 and y == 0) or (x == 0 and y == ylen-1) or (x == xlen-1 and y == 0) or (x == xlen-1 and y == ylen-1):
        dim = (2,2)
    
    # Top/Bottom edges have 2x3 neighbor arrays
    elif (y == 0 or y == ylen-1):
        dim = (2,3)

    # Left/Right edges have 3x2 neighbor arrays
    elif (x == 0 or x == xlen-1):
        dim = (3,2)

    # Everything thats not an edge or corner is regular 3x3 neighbor array
    else:
        dim = (3,3)

    # Now we calculate the "distance" between (x,y) and every other point on "board"
    grid = np.mgrid[0:ylen, 0:xlen]

    ygrid = grid[0]
    xgrid = grid[1]

    ydist = (ygrid - y)**2
    xdist = (xgrid - x)**2

    dist = np.sqrt(ydist + xdist)

    # If the distance is less than/equal to sqrt(2) (1.42 slightly > sqrt(2)), then it is a neighbor
    index = (dist < 1.42)

    # Boolean array indexing returns 1D array, so we need to reshape
    # Returns a neighbor array as well as their indices in "board"
    return board[index].reshape(dim), np.where(index==True)



def get_proba(board):
    probas = np.zeros_like(board, dtype=np.float)
    
    # For each hidden tile, calulate probability
    for r in range(len(board)):
        for c in range(len(board[0])):

            # Only calculate probabilities for 1s,2s,3s etc...
            if board[r][c] != -1 and board[r][c] != 0:

                # Get neighbors and indices
                neighs, indices = get_neigh(board,c,r)

                num_zeros = (neighs==0).sum()   # How many neighbors are hidden
                if num_zeros == 0:              # If no hidden neighbors, skip
                    continue

                num_bombs = board[r][c]         # The middle number is how many bombs are neighbors
                p = num_bombs / num_zeros       # Proabability = num bombs / num hidden tiles

                # Add "p" to all hidden neighbors
                for row, col in zip(indices[0], indices[1]):
                    if board[row][col] == 0:       # If tile is hidden
                        probas[row][col] += p      # Add proabability
    
    return probas




def proba_helper(arr):
    pass