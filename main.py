# -------------------------------------------
# Maze Solver V2.0
# Author: Timothy Foreman
# Date last modified: 12/23/2020
# -------------------------------------------
from PIL import Image
import pygame
import time
import os

IMAGE_REF = "images/maze (13).gif"
# IMAGE_REF = "images/maze (12).gif"

IMAGE_SCALE = 30
# IMAGE_SCALE = 30
START_COLOR = (0, 255, 100)
FINISH_COLOR = (0, 255, 100)
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

# Collect image data
for _x in range(image_width):
    for _y in range(image_height):
        pixel = Pixel(_x, _y, color_value[_x, _y])
        entire_col.append(pixel)
    grid.append(entire_col)
    entire_col = []

# Find entrances

# Search rows
for i in range(1, image_width - 1):
    # Top row
    if grid[i][1].color == 0:
        entrances.append(grid[i][1])
    # Bottom row
    if grid[i][image_height - 2].color == 0:
        entrances.append(grid[i][image_height - 2])

# Search cols
for i in range(1, image_height - 1):
    # Left col
    if grid[1][i].color == 0:
        entrances.append(grid[1][i])

    # Right col
    if grid[image_width - 2][i].color == 0:
        entrances.append(grid[image_width - 2][i])

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


def add_color_gradient():
    colors = []
    spaces = len(successful_path)
    for i in range(spaces):
        num = round(510 / spaces * i)
        if num < 256:
            colors.append((255 - num, 0, 0))
        else:
            colors.append((0, 0, abs(255 - num)))

    counter = 0
    for i in successful_path:
        draw_pixel(i[0], i[1], colors[counter])
        counter += 1


def depth_first_search():
    global current_pos
    global previous_pos
    global fork_pos
    global fork_pos_previous
    global possible_paths
    global successful_path
    global pixels_traversed
    global num_forks

    paths = get_paths(current_pos)

    # Remove previous
    for i in paths:
        if (i.x, i.y) == (previous_pos.x, previous_pos.y):
            paths.remove(i)
    num_paths = len(paths)

    # Scary code here
    if num_paths == 3:
        paths.pop()
    num_paths = len(paths)

    if num_paths == 1:
        previous_pos = current_pos
        current_pos = paths[0]
        successful_path.append((current_pos.x, current_pos.y))  # add to successful path
        pixels_traversed += 1
        draw_pixel(current_pos.x, current_pos.y, PATH_COLOR)

    elif num_paths == 2:
        num_forks += 1
        fork_pos.append(current_pos)  # add fork pos to list
        fork_pos_previous.append(previous_pos)  # add previous fork pos to list
        for i in paths:
            possible_paths.append(i)  # add possible paths to list

        # go down most recent option, possible_paths[-1]
        current_pos = possible_paths[-1]  # select recent path
        pixels_traversed += 1
        successful_path.append((current_pos.x, current_pos.y))  # add to successful path
        draw_pixel(current_pos.x, current_pos.y, PATH_COLOR)  # color recent tan to red
        possible_paths.pop()  # remove chosen path from list
        previous_pos = fork_pos[-1]  # make previous the fork pos of the most recent fork


    elif num_paths == 0:
        index = successful_path.index((fork_pos[-1].x, fork_pos[-1].y)) + 1
        # index = successful_path.index((fork_pos[-1].x, fork_pos[-1].y))
        failed_path = successful_path[index:]
        for i in failed_path:
            draw_pixel(i[0], i[1], (255, 255, 255))
        successful_path = successful_path[:index]  # locked

        current_pos = possible_paths[-1]  # go back to most recent fork, take other path
        pixels_traversed += 1
        successful_path.append((current_pos.x, current_pos.y))  # add to successful path
        draw_pixel(current_pos.x, current_pos.y, PATH_COLOR)  # color it red
        possible_paths.pop()  # remove chosen path from possibilities
        previous_pos = fork_pos[-1]  # select previous as fork pos
        fork_pos.pop()  # remove this fork

    # Base case
    if is_at_finish(current_pos):
        end_time = time.time()
        print(f"Solved in {end_time - start_time} seconds")
        print(f"Forks encountered: {num_forks}")
        print(f"Pixels traversed: {pixels_traversed}")
        add_color_gradient()
        draw_pixel(finish.x, finish.y, FINISH_COLOR)
        draw_pixel(start.x, start.y, START_COLOR)
        pygame.image.save(display_surface, "MAZE_SOLUTION.png")
        pygame.quit()
        os.startfile(r"C:\Users\Timothy\PycharmProjects\maze_solver\index.html")
        exit()


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
pygame.image.save(display_surface, "MAZE.png")

current_pos = start
previous_pos = start
fork_pos = []
fork_pos_previous = []
possible_paths = []
successful_path = [(start.x, start.y)]
num_forks = 0
pixels_traversed = 0

# print(f"Start: {start}")
# print(f"End: {finish}")

start_time = time.time()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_DOWN:
        #         solve()

    # clock.tick(30)
    depth_first_search()
    pygame.display.update()

# -------------------------------------------
