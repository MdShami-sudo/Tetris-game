import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]  # L
]

# Colors for each shape
SHAPE_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cute Tetris")

# Clock to control game speed
clock = pygame.time.Clock()

# Function to create a grid
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                c = locked_positions[(x, y)]
                grid[y][x] = c
    return grid

# Function to draw grid
def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Function to get a random shape
def get_shape():
    return random.choice(SHAPES), random.choice(SHAPE_COLORS)

# Function to draw the window
def draw_window(surface, grid, score=0):
    surface.fill(BLACK)
    draw_grid(surface, grid)
    pygame.display.update()

# Function to check if position is valid
def valid_space(shape, grid, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                try:
                    if grid[y + off_y][x + off_x] != BLACK:
                        return False
                except IndexError:
                    return False
    return True

# Function to rotate shape
def rotate(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

# Main function
def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    current_shape, current_color = get_shape()
    current_pos = [SCREEN_WIDTH // BLOCK_SIZE // 2 - len(current_shape[0]) // 2, 0]

    change_shape = False
    score = 0
    fall_time = 0
    fall_speed = 0.27

    running = True
    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_pos[1] += 1
            if not valid_space(current_shape, grid, current_pos):
                current_pos[1] -= 1
                change_shape = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_pos[0] -= 1
                    if not valid_space(current_shape, grid, current_pos):
                        current_pos[0] += 1
                if event.key == pygame.K_RIGHT:
                    current_pos[0] += 1
                    if not valid_space(current_shape, grid, current_pos):
                        current_pos[0] -= 1
                if event.key == pygame.K_DOWN:
                    current_pos[1] += 1
                    if not valid_space(current_shape, grid, current_pos):
                        current_pos[1] -= 1
                if event.key == pygame.K_UP:
                    current_shape = rotate(current_shape)
                    if not valid_space(current_shape, grid, current_pos):
                        current_shape = rotate(current_shape)
                        current_shape = rotate(current_shape)
                        current_shape = rotate(current_shape)

        shape_pos = [(x + current_pos[0], y + current_pos[1]) for y, row in enumerate(current_shape) for x, cell in enumerate(row) if cell]

        for pos in shape_pos:
            p_x, p_y = pos
            if p_y > -1:
                grid[p_y][p_x] = current_color

        if change_shape:
            for pos in shape_pos:
                p_x, p_y = pos
                locked_positions[(p_x, p_y)] = current_color
            current_shape, current_color = get_shape()
            current_pos = [SCREEN_WIDTH // BLOCK_SIZE // 2 - len(current_shape[0]) // 2, 0]
            change_shape = False
            if not valid_space(current_shape, grid, current_pos):
                running = False

        draw_window(screen, grid)

if __name__ == "__main__":
    main()
