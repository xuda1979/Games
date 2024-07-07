import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
TILE_SIZE = 60
GRID_WIDTH, GRID_HEIGHT = 8, 8
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Color Match Adventure')

# Functions
def create_grid():
    return [[random.choice(COLORS) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, grid[y][x], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

def swap_tiles(grid, pos1, pos2):
    grid[pos1[1]][pos1[0]], grid[pos2[1]][pos2[0]] = grid[pos2[1]][pos2[0]], grid[pos1[1]][pos1[0]]

def check_matches(grid):
    matches = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH - 2):
            if grid[y][x] == grid[y][x + 1] == grid[y][x + 2]:
                matches.append((x, y))
                matches.append((x + 1, y))
                matches.append((x + 2, y))
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT - 2):
            if grid[y][x] == grid[y + 1][x] == grid[y + 2][x]:
                matches.append((x, y))
                matches.append((x, y + 1))
                matches.append((x, y + 2))
    return list(set(matches))

def remove_matches(grid, matches):
    for (x, y) in matches:
        grid[y][x] = None

def drop_tiles(grid):
    for x in range(GRID_WIDTH):
        empty_slots = 0
        for y in range(GRID_HEIGHT - 1, -1, -1):
            if grid[y][x] is None:
                empty_slots += 1
            elif empty_slots > 0:
                grid[y + empty_slots][x] = grid[y][x]
                grid[y][x] = None
        for y in range(empty_slots):
            grid[y][x] = random.choice(COLORS)

# Main game loop
grid = create_grid()
selected_tile = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x, y = x // TILE_SIZE, y // TILE_SIZE
            if selected_tile is None:
                selected_tile = (x, y)
            else:
                swap_tiles(grid, selected_tile, (x, y))
                matches = check_matches(grid)
                if matches:
                    remove_matches(grid, matches)
                    drop_tiles(grid)
                else:
                    swap_tiles(grid, selected_tile, (x, y))  # Swap back if no match
                selected_tile = None

    screen.fill((255, 255, 255))
    draw_grid(grid)
    pygame.display.flip()

pygame.quit()
