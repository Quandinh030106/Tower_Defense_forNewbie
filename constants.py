import pygame

# Initialize Pygame
pygame.init()
pygame.font.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 40
GAME_FONT = pygame.font.SysFont('Arial', 20)
TITLE_FONT = pygame.font.SysFont('Arial', 32)
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
PURPLE = (200, 50, 200)
BROWN = (139, 69, 19)
GRAY = (100, 100, 100)
DARK_GREEN = (0, 100, 0)

# Path definition (grid coordinates)
PATH = [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), 
        (5, 4), (5, 5), (5, 6), (5, 7), 
        (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),
        (10, 6), (10, 5), (10, 4), (10, 3), (10, 2),
        (11, 2), (12, 2), (13, 2), (14, 2), (15, 2),
        (15, 3), (15, 4), (15, 5), (15, 6), (15, 7),
        (16, 7), (17, 7), (18, 7), (19, 7)] 