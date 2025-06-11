import pygame
import sys
from game import Game
from ui.welcome_screen import WelcomeScreen
from ui.map_selection import MapSelection
from ui.difficulty_selection import DifficultySelection
from constants import *

def main():
    # Initialize Pygame
    pygame.init()
    pygame.font.init()
    
    # Create initial window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense 8-bit")
    
    # Create welcome screen
    welcome_screen = WelcomeScreen(screen)
    map_selection = None
    difficulty_selection = None
    
    # Game state
    current_game = None
    is_fullscreen = False
    current_screen = "welcome"  # Can be "welcome", "map", "difficulty", or "game"
    selected_map = None
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if current_screen == "welcome":
                        action = welcome_screen.handle_click(event.pos)
                        if action == "play":
                            current_screen = "map"
                            map_selection = MapSelection(screen)
                        elif action == "quit":
                            running = False
                            
                    elif current_screen == "map":
                        action, map_name = map_selection.handle_click(event.pos)
                        if action == "next":
                            current_screen = "difficulty"
                            selected_map = map_name
                            difficulty_selection = DifficultySelection(screen, selected_map)
                        elif action == "back":
                            current_screen = "welcome"
                            
                    elif current_screen == "difficulty":
                        action, map_name, difficulty = difficulty_selection.handle_click(event.pos)
                        if action == "start":
                            current_screen = "game"
                            current_game = Game(map_name, difficulty)
                        elif action == "back":
                            current_screen = "map"
                            
                    elif current_screen == "game":
                        if current_game.game_over:
                            restart_button = current_game.draw_game_over()
                            if restart_button and restart_button.collidepoint(event.pos):
                                current_game.reset_game()
                        else:
                            # Handle game clicks
                            tower_type, cost = current_game.menu.handle_click(event.pos, current_game.gold)
                            if tower_type:
                                if tower_type == "quit":
                                    current_screen = "welcome"
                                    current_game = None
                                elif tower_type == "start_wave":
                                    current_game.start_wave()
                                else:
                                    current_game.selected_tower_type = tower_type
                                    current_game.selected_tower = None
                            else:
                                # Handle unit selection and tower placement
                                x, y = event.pos
                                if x < SCREEN_WIDTH - 200:
                                    grid_x = x // GRID_SIZE
                                    grid_y = y // GRID_SIZE
                                    
                                    if current_game.selected_tower_type:
                                        if current_game.place_tower(grid_x, grid_y):
                                            current_game.selected_tower_type = None
                                    elif current_game.dragging_unit is None:
                                        clicked_on_unit = False
                                        for tower in current_game.towers:
                                            if tower.grid_x == grid_x and tower.grid_y == grid_y:
                                                if current_game.selected_unit:
                                                    current_game.selected_unit.is_selected = False
                                                tower.is_selected = True
                                                current_game.selected_unit = tower
                                                tower.start_drag(x, y)
                                                current_game.dragging_unit = tower
                                                clicked_on_unit = True
                                                break
                                        
                                        if not clicked_on_unit:
                                            for soldier in current_game.soldiers:
                                                if soldier.grid_x == grid_x and soldier.grid_y == grid_y:
                                                    if current_game.selected_unit:
                                                        current_game.selected_unit.is_selected = False
                                                    soldier.is_selected = True
                                                    current_game.selected_unit = soldier
                                                    soldier.start_drag(x, y)
                                                    current_game.dragging_unit = soldier
                                                    clicked_on_unit = True
                                                    break
                                            
                                            if not clicked_on_unit:
                                                if current_game.selected_unit:
                                                    current_game.selected_unit.is_selected = False
                                                    current_game.selected_unit = None
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if current_screen == "game" and current_game and current_game.dragging_unit:
                    x, y = pygame.mouse.get_pos()
                    if x < SCREEN_WIDTH - 200:
                        grid_x = x // GRID_SIZE
                        grid_y = y // GRID_SIZE
                        
                        if current_game.is_valid_tower_position(grid_x, grid_y):
                            current_game.dragging_unit.end_drag(grid_x, grid_y)
                        else:
                            current_game.dragging_unit.end_drag(
                                current_game.dragging_unit.grid_x,
                                current_game.dragging_unit.grid_y
                            )
                    
                    if current_game.selected_unit:
                        current_game.selected_unit.is_selected = False
                        current_game.selected_unit = None
                    current_game.dragging_unit = None
            
            elif event.type == pygame.MOUSEMOTION:
                if current_screen == "game" and current_game and current_game.dragging_unit:
                    x, y = pygame.mouse.get_pos()
                    current_game.dragging_unit.update_drag(x, y)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_screen == "game":
                        if current_game.selected_unit:
                            current_game.selected_unit.is_selected = False
                            current_game.selected_unit = None
                        current_game.selected_tower_type = None
                        current_game.dragging_unit = None
                    else:
                        running = False
        
        # Update and draw
        if current_screen == "welcome":
            welcome_screen.draw()
        elif current_screen == "map":
            map_selection.draw()
        elif current_screen == "difficulty":
            difficulty_selection.draw()
        elif current_screen == "game":
            if not current_game.game_over:
                current_game.update()
            current_game.draw()
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        pygame.time.Clock().tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
