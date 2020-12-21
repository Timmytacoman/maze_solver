# -------------------------------------------
# Maze Solver V1.0
# Author: Timothy Foreman
# Date last modified: 12/20/2020
# -------------------------------------------
import math
from PIL import Image
import numpy as np
import pygame
import time


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
        return f"x: {self.x}\ny: {self.y}\ncolor: {self.color}\nis_entrance: {self.is_entrance}\n"


# -------------------------------------------
maze_image = "images/maze (1).gif"
im = Image.open(maze_image)
pix = im.load()
width, height = im.size

# create 2d array of Pixel objects, INCLUDING WHITE LINE
grid = []
line = []

# white is 0


for row in range(height):
    for col in range(width):
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

# -------------------------------------------


# print(Pixel.entrances[0], Pixel.entrances[1])
# use pygame?

# 825 x 500 matches preview
window_width = 825
window_height = 500

pygame.init()
# window = pygame.display.set_mode((width, height))
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("maze_solver")
clock = pygame.time.Clock()

image = pygame.image.load(maze_image)
image_width, image_height = image.get_size()
big_image = pygame.transform.scale(image, (window_width, window_height))

scale = window_width / image_width

window.blit(big_image, (0, 0))


# -------------------------------------------


def get_surrounding(pixel):
    x_pos = pixel.x
    y_pos = pixel.y
    # print(x_pos, y_pos)

    # north = grid[row][col]
    north = grid[y_pos - 1][x_pos]
    east = grid[y_pos][x_pos + 1]
    south = grid[y_pos + 1][x_pos]
    west = grid[y_pos][x_pos - 1]

    return [north, east, south, west]


def draw_pixel(x, y, color):
    pygame.draw.rect(window, color, (x * scale, y * scale, scale, scale))


def check_surrounding_paths(pixel):
    adjacent = get_surrounding(pixel)
    open_paths = []
    for i in adjacent:
        if i.color == 0 and (i.x != 0 and i.x != width - 1) and (
                i.y != 0 and i.y != height - 1):  # white and not border
            open_paths.append(i)

    return open_paths


# possibilities = check_surrounding_paths(Pixel.entrances[0])
# for i in possibilities:
#     print(i)
#     draw_pixel(i.x, i.y, (0, 255, 255))


draw_pixel(Pixel.entrances[0].x, Pixel.entrances[0].y, (0, 255, 0))
draw_pixel(Pixel.entrances[1].x, Pixel.entrances[1].y, (0, 255, 0))

current_pixel = Pixel.entrances[0]

previous_positions = []
splits = []
current_successful_path = []

crashed = False

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        # print(event)

    pygame.display.update()
    clock.tick(60)

    possibilities = check_surrounding_paths(current_pixel)

    for i in possibilities:
        if (i.x, i.y) in previous_positions:  # remove spot that I came from
            possibilities.remove(i)

    if len(possibilities) == 1:  # one possible path
        # print("making move")
        previous_positions.append((current_pixel.x, current_pixel.y))  # add previous position into memory
        current_pixel = possibilities[0]  # move to open spot
        draw_pixel(current_pixel.x, current_pixel.y, (255, 0, 0))  # draw pixel on current spot

    elif len(possibilities) == 2:
        print("Fork")
        # arrived at fork
        # keep track of journey
        current_successful_path.append(previous_positions)

        # mark confirmed path with a different color
        for i in previous_positions:
            # print(i)
            draw_pixel(i[0], i[1], (100, 200, 0))

        # reset previous positions
        previous_positions = [previous_positions[-1]]

        splits.append((current_pixel.x, current_pixel.y))

        # select a path to continue through
        previous_positions.append((current_pixel.x, current_pixel.y))  # add previous position into memory
        current_pixel = possibilities[1]
        previous_positions.append((current_pixel.x, current_pixel.y))  # add previous position into memory
        draw_pixel(current_pixel.x, current_pixel.y, (255, 0, 0))  # draw pixel on current spot



    elif len(possibilities) == 0:
        print("Dead end")
        # dead end, reset failed track color
        previous_positions.append((current_pixel.x, current_pixel.y))
        for i in previous_positions:
            draw_pixel(i[0], i[1], (255, 255, 255))
        previous_positions = previous_positions[:3]

        # move to fork
        current_pixel = grid[splits[0][1]][splits[0][0]]
        draw_pixel(current_pixel.x, current_pixel.y, (133, 25, 0))

