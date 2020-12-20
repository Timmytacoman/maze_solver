# -------------------------------------------
# Maze Solver V1.0
# Author: Timothy Foreman
# Date last modified: 12/19/2020
# -------------------------------------------


from PIL import Image
import pygame


# -------------------------------------------

# Use OOP for each pixel (x, y, surrounding etc)
class Pixel:
    """Pixel class for each pixel in the maze image"""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def __str__(self):
        return f"x: {self.x}\ny: {self.y}\ncolor: {self.color}"


# -------------------------------------------


def setup_maze():
    """Setup maze function to create 2d array for each pixel object.
        Returns the maze array as well as the original maze dimensions."""
    # load image pixels
    im = Image.open('images/first_maze.png')
    pix = im.load()

    # get image size
    width, height = im.size

    row = []
    grid = []

    # get each pixel rgb
    for y_pos in range(height):
        for x_pos in range(width):
            rgb_value = pix[x_pos, y_pos]
            # create pixel object
            row.append(Pixel(x_pos, y_pos, rgb_value))
        grid.append(row)
        row = []

    return grid, width, height


# -------------------------------------------


def find_starting_position():
    for i in maze[-1]:
        if i.color == (255, 255, 255):
            return i


# -------------------------------------------

# globals
maze, x_len, y_len = setup_maze()
starting_pixel = find_starting_position()

# -------------------------------------------

# pygame part
pygame.init()
maze_image = pygame.image.load("images/first_maze.png")
game_display = pygame.display.set_mode((x_len, y_len))
clock = pygame.time.Clock()


def draw_original_maze():
    game_display.blit(maze_image, (0, 0))

def draw_location(x, y):
    width = 5
    height = 5
    pygame.draw.rect(game_display, (255, 0, 0), (x, y, width, height))

def left_turn_algorithm():
    current_pixel = starting_pixel
    # move left



done = False

# draw original maze
draw_original_maze()


# game loop
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    draw_location(starting_pixel.x, starting_pixel.y)
    left_turn_algorithm()

    pygame.display.update()
    clock.tick(60)

# -------------------------------------------
