# Standard Imports

# 3rd Party Imports
import numpy as np



class Board():
    """
    A class to represent a minesweeper board
    """

    def __init__(self,dim, n_mines):

        self.x_dim = dim[1]
        self.y_dim = dim[0]
        self.data = np.zeros((self.x_dim, self.y_dim))


    def __repr__(self):
        return str(self.data)









