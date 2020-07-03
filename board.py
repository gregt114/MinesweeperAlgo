# Standard Imports

# 3rd Party Imports
import numpy as np
import pyautogui as pg


class Board():
    """
    A class to represent a minesweeper board
    """

    def __init__(self, dim, n_mines):

        self.nrows = dim[1]
        self.ncols = dim[0]
        self.n_mines = n_mines
        self.bombs = []             # List of tuple indicies for marked bombs


    def __repr__(self):
        if self.data.any():
            return str(self.data)
        else:
            return "<Board Object>"

    
    def find_window(self):
        """
        Sets left, top, width, and height of window
        """
        window = pg.locateOnScreen("images/blank_board.png", confidence=0.95)
        
        self.window = (window.left, window.top, window.width, window.height)


    def test_click(self):
        """
        Click the first hidden tile found(for dev purposes only)
        """
        self.click_tile(0,0)

    
    def get_coords(self, row ,col):
        """
        Returns (x,y) coordinates of a tile given its (row,col) index
        """
        return (self.window[0] + 17*col + 8.5, self.window[1] + 17*row + 8.5)
        
    
    def click_tile(self, row, col):
        """
        Uses pyautogui to click on the specified tile
        """
        coords = self.get_coords(row, col)
        x = coords[0]
        y = coords[1]

        pg.click(x=x,y=y)


    def mark_bomb(self, row, col):
        """
        Uses pyautogui to mark the specified bomb
        """
        coords = self.get_coords(row, col)
        x = coords[0]
        y = coords[1]

        pg.rightClick(x=x,y=y)

        self.bombs.append((row, col))   # Add bomb location to list of bombs

    
    def read_board(self, window):
        """
        Returns 2D numpy array of the board
        -1 : Clear tile
        0  : Hidden tile
        1  : One neighbor is a bomb
        2  : Two neighbors are bombs
        3,4,5 etc...
        9  : Bomb(flagged)
        """

        # Get locations for each type of tile
        clears = list(pg.locateAllOnScreen("images/clear.png", region=window, confidence=0.95))
        hiddens = list(pg.locateAllOnScreen("images/hidden.png", region=window, confidence=0.95))
        ones = list(pg.locateAllOnScreen("images/one.png", region=window, confidence=0.95))
        twos = list(pg.locateAllOnScreen("images/two.png", region=window, confidence=0.95))
        threes = list(pg.locateAllOnScreen("images/three.png", region=window, confidence=0.95))
        fours = list(pg.locateAllOnScreen("images/four.png", region=window, confidence=0.95))
        fives = list(pg.locateAllOnScreen("images/five.png", region=window, confidence=0.95))
        bombs = list(pg.locateAllOnScreen("images/flag.png", region=window, confidence=0.95))

        
        board_data = []
        # Add labels to each type of tile (Box objects)
        # -1 is a clear tile, 0 is a hidden tile, 1 is one, etc...
        for lst,name in zip([clears, hiddens, ones, twos, threes, fours, fives, bombs], [-1,0,1,2,3,4,5,9]):
            for tile in lst:
                board_data.append([tuple(pg.center(tile)), name])

        # Sort data by positiion(first by y position, then by x for ties)
        board_sorted = sorted(board_data, key=lambda x: (x[0][1],x[0][0]))

        # Create array that represents the minesweeper board and fill it
        final = np.empty(self.nrows * self.ncols, dtype=int)
        for i in range(len(final)):
            final[i] = board_sorted[i][1]
        
        # Reshape the 1D array into the correct matrix shape
        final = final.reshape(self.nrows, self.ncols)

        self.data = final

    
    def get_neigh(self, row, col):
        """
        Returns the neighbors of the tile specified by (row,col)
        as well as their indices
        """

        ylen, xlen = self.nrows, self.ncols

        # We first need to find the corrext shape for the array
        # Corners
        if (col == 0 and row == 0) or (col == 0 and row == ylen-1) or (col == xlen-1 and row == 0) or (col == xlen-1 and row == ylen-1):
            dim = (2,2)
        
        # Top/Bottom edges have 2x3 neighbor arrays
        elif (row == 0 or row == ylen-1):
            dim = (2,3)

        # Left/Right edges have 3x2 neighbor arrays
        elif (col == 0 or col == xlen-1):
            dim = (3,2)

        # Everything thats not an edge or corner is regular 3x3 neighbor array
        else:
            dim = (3,3)

        # Now we calculate the "distance" between (x,y) and every other point on "board"
        grid = np.mgrid[0:ylen, 0:xlen]

        ygrid = grid[0]
        xgrid = grid[1]

        ydist = (ygrid - row)**2
        xdist = (xgrid - col)**2

        dist = np.sqrt(ydist + xdist)

        # If the distance is less than/equal to sqrt(2) (1.42 slightly > sqrt(2)), then it is a neighbor
        index = (dist < 1.42)

        # Boolean array indexing returns 1D array, so we need to reshape
        # Returns a neighbor array as well as their indices in "board"
        return self.data[index].reshape(dim), np.where(index==True)

    
    def reduce_board(self):
        """
        Returns self.data but processed so that labels are replaced with
        the effective label
        """
        effective = self.data.copy()

        # For each bomb tile
        for r in range(self.data.shape[0]):
            for c in range(self.data.shape[1]):
                if self.data[r][c] == 9:
                    
                    # Get neighbors and their (r,c) locations
                    neighs, indices = self.get_neigh(r, c)
                    locs = zip(indices[0], indices[1])

                    # For each labeled tile thats a neighbor, decrease label by 1
                    for row, col in locs:
                        if effective[row][col] > 0 and effective[row][col] < 9:

                            # If tile is decreased from 1 to 0, make it -1 instead bc -1 means a clear tile.  Else subtract 1 regularly
                            if effective[row][col] == 1:
                                effective[row][col] = -1
                            else:
                                effective[row][col] -= 1
        
        self.data = effective



    def get_scores(self):
        scores = np.zeros_like(self.data, dtype=np.float)

        # For each...
        for r in range(self.data.shape[0]):
            for c in range(self.data.shape[1]):

                # Labeled tiles
                if self.data[r][c] > 0:
                    # Get neighbors and their (r,c) locations
                    neighs, indices = self.get_neigh(r, c)
                    locs = zip(indices[0], indices[1])


                    # Deterministic rules for mines
                    
                    center = self.data[r][c]            # Tile in consideration
                    hidden = (neighs==0).sum()      # Num hidden neighbors
                    clear = (neighs==-1).sum()      # Num clear neighbors
                    flagged = (neighs==9).sum()     # Num flagged neighbors


                    # Rule 1: If center num - num flagged = num hidden, each hidden is a bomb
                    if center - flagged == hidden:
                        for row, col in locs:
                            if self.data[row][col] == 0:
                                scores[row][col] = 100


                # Bomb tiles
                if self.data[r][c] == 9:
                    pass


        return scores


    def make_move(self):
        pass



