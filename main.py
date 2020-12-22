# -------------------------------------------
# Maze Solver V2.0
# Author: Timothy Foreman
# Date last modified: 12/21/2020
# -------------------------------------------
from PIL import Image
import pygame
import time

IMAGE_REF = "images/maze.gif"
IMAGE_SCALE = 10
START_COLOR = (196, 255, 14)
FINISH_COLOR = (236, 28, 36)
PATH_COLOR = (236, 28, 36)
FORK_COLOR = (0, 168, 243)
PREVIOUS_COLOR = (255, 174, 200)
POSSIBLE_PATH_COLOR = (253, 236, 166)


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
start = entrances[1]
finish = entrances[0]


# -------------------------------------------

def draw_pixel(x, y, color):
    pygame.draw.rect(display_surface, color, (x * IMAGE_SCALE, y * IMAGE_SCALE, IMAGE_SCALE, IMAGE_SCALE))


def is_at_finish(pixel1):
    if (pixel1.x == finish.x) and (pixel1.y == finish.y):
        return True
    return False


def get_paths(pixel):
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
        if i.x == image_width - 1 or i.y == image_height - 1:
            viable_paths.remove(i)

    return viable_paths


def solve():
    global current_pos
    global previous_pos
    global fork_pos
    global fork_pos_previous
    global possible_paths

    # Base case
    if is_at_finish(current_pos):
        print("done")
        exit()

    paths = get_paths(current_pos)

    # Remove previous
    for i in paths:
        if (i.x, i.y) == (previous_pos.x, previous_pos.y):
            paths.remove(i)

    # for i in paths:
    #     print(i)
    # print()

    num_paths = len(paths)

    if num_paths == 1:
        previous_pos = current_pos
        current_pos = paths[0]
        draw_pixel(current_pos.x, current_pos.y, PATH_COLOR)

    elif num_paths == 2:
        print("At fork")
        fork_pos.append(current_pos)  # add fork pos to list
        draw_pixel(current_pos.x, current_pos.y, FORK_COLOR)  # mark fork as blue
        fork_pos_previous.append(previous_pos)  # add previous fork pos to list
        draw_pixel(previous_pos.x, previous_pos.y, PREVIOUS_COLOR)  # mark previous as pink
        for i in paths:
            possible_paths.append(i)  # add possible paths to list
            draw_pixel(i.x, i.y, POSSIBLE_PATH_COLOR)  # color possible paths

        # go down most recent option, possible_paths[-1]
        current_pos = possible_paths[-1]  # select recent path
        draw_pixel(current_pos.x, current_pos.y, PATH_COLOR)  # color recent tan to red
        possible_paths.pop()  # remove chosen path from list
        previous_pos = fork_pos[-1]  # make previous the fork pos of the most recent fork


    elif num_paths == 0:
        current_pos = possible_paths[-1]  # go back to most recent fork, take other path
        draw_pixel(current_pos.x, current_pos.y, PATH_COLOR)  # color it red
        possible_paths.pop()  # remove chosen path from possibilities
        previous_pos = fork_pos[-1]  # select previous as fork pos
        fork_pos.pop()  # remove this fork


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

current_pos = start
previous_pos = start
fork_pos = []
fork_pos_previous = []
possible_paths = []

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_DOWN:
        #         solve()

    # clock.tick(40)
    pygame.display.update()

    solve()

# -------------------------------------------
