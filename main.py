# -------------------------------------------
# Maze Solver V1.0
# Author: Timothy Foreman
# Date last modified: 12/19/2020
# -------------------------------------------

from PIL import Image
import numpy as np


# -------------------------------------------


class Pixel:
    """Pixel class for each pixel in the maze image"""

    entrances = []

    def __init__(self, x, y, color, is_entrance):
        self.x = x
        self.y = y
        self.color = color
        self.is_entrance = is_entrance

    def __str__(self):
        return f"x: {self.x}\ny: {self.y}\ncolor: {self.color}\nis_entrance: {is_entrance}"


# -------------------------------------------

im = Image.open("images/maze.png")
pix = im.load()
width, height = im.size

# create 2d array of Pixel objects, INCLUDING WHITE LINE
grid = []
line = []

# white is 0


for row in range(width):
    for col in range(height):
        # x = col, y = row
        # get color
        color = pix[col, row]
        # check if is entrance on border
        is_entrance = False
        if color == 0:
            if (col != 0 and col != width - 1) and (row != 0 and row != height - 1):
                if (col == 1 or col == width - 2) or (row == 1 or row == height - 2):
                    # is entrance
                    is_entrance = True
        # add to line
        line.append(Pixel(col, row, color, is_entrance))
        # append to separate list for entrances
        if is_entrance:
            Pixel.entrances.append(Pixel(col, row, color, is_entrance))
    # add line row to grid
    grid.append(line)
    # reset line
    line = []

# convert to numpy array
grid = np.array(grid)


print(Pixel.entrances[0])

# -------------------------------------------
