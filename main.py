# -------------------------------------------
# Maze Solver V2.0
# Author: Timothy Foreman
# Date last modified: 12/20/2020
# -------------------------------------------
import math
from PIL import Image
import numpy as np
import pygame
import time

IMAGE_REF = "images/maze (2).gif"
IMAGE_SCALE = 10
START_COLOR = (100, 255, 100)
FINISH_COLOR = (100, 100, 255)
PATH_COLOR = (255, 100, 100)


# -------------------------------------------

class Pixel:
    """Pixel class for each pixel in the maze image"""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color  # 0: White | 1: Black

    def __str__(self):
        return f"Pixel: [{self.x}, {self.y}] | Color: {self.color}"


# -------------------------------------------

# Setup image
image = Image.open(IMAGE_REF)
image_width, image_height = image.size
color_value = image.load()

# Lists to hold Pixel objects
entire_col = []
grid = []
entrances = []

# Collect image data, marking entrances as such
for _x in range(image_width):
    for _y in range(image_height):
        pixel = Pixel(_x, _y, color_value[_x, _y])
        entire_col.append(pixel)
        if color_value[_x, _y] == 0:
            if (_x == 1 or _x == image_width - 2) and (_y != 0 and _y != image_height - 1):
                entrances.append(pixel)
            if (_y == 1 or _y == image_width - 2) and (_x != 0 and _x != image_height - 1):
                entrances.append(pixel)

    grid.append(entire_col)
    entire_col = []

# Declarations
start = entrances[0]
finish = entrances[1]


# -------------------------------------------

def draw_pixel(x, y, color):
    pygame.draw.rect(display_surface, color, (x * IMAGE_SCALE, y * IMAGE_SCALE, IMAGE_SCALE, IMAGE_SCALE))


def is_at_finish(pixel1):
    if (pixel1.x == finish.x) and (pixel1.y == finish.y):
        return True
    return False


def find_viable_paths(pixel):
    # Setup search for paths
    viable_paths = []
    x_pos = pixel.x
    y_pos = pixel.y
    north = grid[x_pos][y_pos - 1]
    east = grid[x_pos + 1][y_pos]
    south = grid[x_pos][y_pos + 1]
    west = grid[x_pos - 1][y_pos]
    directions = [north, south, east, west]

    # Check color
    for i in directions:
        if i.color == 0:
            viable_paths.append(i)

    # Remove borders
    for i in viable_paths:
        if i.x == 0 or i.y == 0:
            viable_paths.remove(i)

    return viable_paths


# def search(pixel):
#     pathing = []
#     current_position = pixel
#     paths = [1]
#     while len(paths) == 1:
#         paths = find_viable_paths(current_position)
#
#         # continue along straight path
#         pathing.append(current_position)
#         current_position = paths[0]
#         draw_pixel(current_position.x, current_position.y, PATH_COLOR)

def solve():
    global behind
    global pos

    # Base case
    if is_at_finish(pos):
        print("YAY!!!!!!!")

    # Setup paths
    paths = find_viable_paths(pos)

    # Remove behind
    if behind is not None:
        for i in paths:
            if (i.x, i.y) == (behind.x, behind.y):
                paths.remove(i)

    # Move along straight line
    if len(paths) == 1:
        behind = pos
        pos = paths[0]
        draw_pixel(pos.x, pos.y, PATH_COLOR)



    else:
        print(len(paths))






# -------------------------------------------

# Pygame setup
pygame.init()
surface_width = image_width * IMAGE_SCALE
surface_height = image_height * IMAGE_SCALE
display_surface = pygame.display.set_mode((surface_width, surface_height))
pygame.display.set_caption("MAZE SOLVER")
clock = pygame.time.Clock()

# Image setup
pg_image = pygame.image.load(IMAGE_REF)
big_image = pygame.transform.scale(pg_image, (surface_width, surface_height))
display_surface.blit(big_image, (0, 0))

# Draw entrances
draw_pixel(start.x, start.y, START_COLOR)
draw_pixel(finish.x, finish.y, FINISH_COLOR)

behind = None
pos = start

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    solve()

    clock.tick(10)
    pygame.display.update()

# -------------------------------------------
