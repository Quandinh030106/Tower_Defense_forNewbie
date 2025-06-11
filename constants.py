import pygame

# Initialize Pygame
pygame.init()
pygame.font.init()

# Get display info for dynamic sizing
display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h
GRID_SIZE = min(SCREEN_WIDTH // 20, SCREEN_HEIGHT // 15)  # Dynamic grid size based on screen dimensions
GAME_FONT = pygame.font.SysFont('Arial', int(SCREEN_HEIGHT * 0.03))  # Dynamic font size
TITLE_FONT = pygame.font.SysFont('Arial', int(SCREEN_HEIGHT * 0.05))  # Dynamic font size
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
ICE = (155, 155, 255)
YELLOW = (255, 255, 50)
PURPLE = (200, 50, 200)
BROWN = (139, 69, 19)
GRAY = (100, 100, 100)
DARK_GREEN = (0, 100, 0)
PINK = (255, 155, 155)
ORANGE = (255, 155, 50)
# Path definition (grid coordinates)
PATH = [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), 
        (5, 4), (5, 5), (5, 6), (5, 7), 
        (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),
        (10, 6), (10, 5), (10, 4), (10, 3), (10, 2),
        (11, 2), (12, 2), (13, 2), (14, 2), (15, 2),
        (15, 3), (15, 4), (15, 5), (15, 6), (15, 7),
        (16, 7), (17, 7), (18, 7), (19, 7)]

PATH_2 = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7),
          (4, 6), (4, 7), (4, 8), (4, 9),
          (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9), (11, 9),
          (11, 8), (11, 7), (11, 6), (11, 5), (11, 4),
          (12, 4), (13, 4), (14, 4), (15, 4), 
          (15, 5), (15, 6), (15, 7), (15, 8),
          (16, 8), (17, 8), (18, 8), (19, 8)]
