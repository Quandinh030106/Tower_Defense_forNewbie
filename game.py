import pygame
import sys
import math
import random
from typing import List, Tuple, Dict, Optional

from constants import *
from tower import Tower, BasicTower, RapidTower, SniperTower
from soldier import Soldier
from enemy import Enemy, BasicEnemy, FastEnemy, TankEnemy
from projectile import Projectile
from menu import Menu

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense 8-bit")
        self.clock = pygame.time.Clock()
        
        self.reset_game()
        
    def reset_game(self):
        self.gold = 100
        self.wave = 1
        self.lives = 10
        self.game_over = False
        self.wave_in_progress = False
        self.towers: List[Tower] = []
        self.soldiers: List[Soldier] = []
        self.enemies: List[Enemy] = []
        self.projectiles: List[Projectile] = []
        self.menu = Menu()
        self.selected_tower_type = None
        self.selected_tower = None
        self.selected_unit = None
        self.dragging_unit = None
    
    def is_valid_tower_position(self, grid_x: int, grid_y: int) -> bool:
        # Check if position is on a path
        if (grid_x, grid_y) in PATH:
            return False
        
        # Check if position is already occupied by a tower
        for tower in self.towers:
            if tower.grid_x == grid_x and tower.grid_y == grid_y:
                return False
                
        # Check if position is already occupied by a soldier
        for soldier in self.soldiers:
            if soldier.grid_x == grid_x and soldier.grid_y == grid_y:
                return False
        
        # Check if position is within game boundaries
        if grid_x < 0 or grid_x >= SCREEN_WIDTH // GRID_SIZE - 5 or grid_y < 0 or grid_y >= SCREEN_HEIGHT // GRID_SIZE:
            return False
            
        return True
    
    def place_tower(self, grid_x: int, grid_y: int) -> bool:
        if not self.is_valid_tower_position(grid_x, grid_y):
            return False
            
        if self.selected_tower_type == "basic_tower" and self.gold >= 50:
            self.towers.append(BasicTower(grid_x, grid_y))
            self.gold -= 50
            return True
        elif self.selected_tower_type == "sniper_tower" and self.gold >= 100:
            self.towers.append(SniperTower(grid_x, grid_y))
            self.gold -= 100
            return True
        elif self.selected_tower_type == "rapid_tower" and self.gold >= 75:
            self.towers.append(RapidTower(grid_x, grid_y))
            self.gold -= 75
            return True
        elif self.selected_tower_type == "soldier" and self.gold >= 30:
            self.soldiers.append(Soldier(grid_x, grid_y))
            self.gold -= 30
            return True
            
        return False
    
    def start_wave(self):
        if not self.wave_in_progress:
            self.wave_in_progress = True
            self.spawn_enemies()
    
    def spawn_enemies(self):
        num_enemies = self.wave * 3 + 5
        
        # Different mix of enemies based on wave number
        num_basic = max(3, num_enemies - self.wave * 2)
        num_fast = min(self.wave, num_enemies // 3)
        num_tank = max(0, min(self.wave // 3, 3))
        
        # Spawn delay between enemies
        self.spawn_delay = 60
        self.spawn_counter = 0
        
        # Prepare enemy queue
        self.enemy_queue = []
        for _ in range(num_basic):
            self.enemy_queue.append("basic")
        for _ in range(num_fast):
            self.enemy_queue.append("fast")
        for _ in range(num_tank):
            self.enemy_queue.append("tank")
            
        # Shuffle queue for variety
        random.shuffle(self.enemy_queue)
    
    def spawn_enemy_from_queue(self):
        if not self.enemy_queue:
            return
            
        enemy_type = self.enemy_queue.pop(0)
        
        if enemy_type == "basic":
            self.enemies.append(BasicEnemy(PATH))
        elif enemy_type == "fast":
            self.enemies.append(FastEnemy(PATH))
        elif enemy_type == "tank":
            self.enemies.append(TankEnemy(PATH))
    
    def update(self):
        # Spawn enemies if wave in progress
        if self.wave_in_progress and self.enemy_queue:
            self.spawn_counter += 1
            if self.spawn_counter >= self.spawn_delay:
                self.spawn_counter = 0
                self.spawn_enemy_from_queue()
        
        # Check if wave is complete
        if self.wave_in_progress and not self.enemy_queue and not self.enemies:
            self.wave_in_progress = False
            self.wave += 1
            self.gold += 30 + (self.wave * 5)  # Gold reward for completing wave
        
        # Update towers
        for tower in self.towers:
            tower.update_cooldown()
            if tower.can_fire():
                target = tower.find_target(self.enemies)
                if target:
                    self.projectiles.append(tower.fire(target))
                    tower.reset_cooldown()
        
        # Update soldiers
        for soldier in self.soldiers[:]:
            soldier.update_cooldown()
            if soldier.can_attack():
                target = soldier.find_target(self.enemies)
                if target:
                    soldier.attack(target)
                    soldier.reset_cooldown()
            
            # Remove dead soldiers
            if soldier.is_dead():
                self.soldiers.remove(soldier)
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            if projectile.move():
                self.projectiles.remove(projectile)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.move()
            
            # Check if enemy reached the end
            if enemy.reached_end:
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.game_over = True
                continue
                
            # Check if enemy is dead
            if enemy.is_dead():
                self.gold += enemy.reward
                self.enemies.remove(enemy)
    
    def draw_grid(self):
        # Draw grid lines
        for x in range(0, SCREEN_WIDTH - 200, GRID_SIZE):
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (SCREEN_WIDTH - 200, y))
    
    def draw_path(self):
        for grid_x, grid_y in PATH:
            pygame.draw.rect(self.screen, BROWN, (grid_x * GRID_SIZE, grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = TITLE_FONT.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Wave reached text
        wave_text = GAME_FONT.render(f"You reached Wave {self.wave}", True, WHITE)
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(wave_text, wave_rect)
        
        # Restart button
        restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 50, 120, 40)
        pygame.draw.rect(self.screen, (70, 70, 70), restart_button)
        pygame.draw.rect(self.screen, BLACK, restart_button, 2)
        
        restart_text = GAME_FONT.render("Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=restart_button.center)
        self.screen.blit(restart_text, restart_rect)
        
        return restart_button
    
    def draw(self):
        # Draw background
        self.screen.fill(DARK_GREEN)
        
        # Draw grid
        self.draw_grid()
        
        # Draw path
        self.draw_path()
        
        # Draw towers
        for tower in self.towers:
            tower.draw(self.screen, tower == self.selected_tower)
        
        # Draw soldiers
        for soldier in self.soldiers:
            soldier.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        
        # Draw menu
        self.menu.draw(self.screen, self.gold, self.wave, self.lives)
        
        # Draw game over screen
        restart_button = None
        if self.game_over:
            restart_button = self.draw_game_over()
            
        # Update display
        pygame.display.flip()
        
        return restart_button
    
    def run(self):
        running = True
        restart_button = None
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if event.button == 1:  # Left click
                        # Check for restart button if game over
                        if self.game_over and restart_button and restart_button.collidepoint(mouse_pos):
                            self.reset_game()
                            continue
                        
                        # Check for menu clicks
                        tower_type, cost = self.menu.handle_click(mouse_pos, self.gold)
                        
                        if tower_type:
                            if tower_type == "quit":
                                running = False
                            elif tower_type == "start_wave":
                                self.start_wave()
                            else:
                                self.selected_tower_type = tower_type
                                self.selected_tower = None
                        else:
                            # Handle unit selection, movement, and tower placement
                            x, y = mouse_pos
                            if x < SCREEN_WIDTH - 200:  # Only allow placement in the game area
                                grid_x = x // GRID_SIZE
                                grid_y = y // GRID_SIZE
                                
                                if self.selected_tower_type:
                                    # Place new tower
                                    if self.place_tower(grid_x, grid_y):
                                        self.selected_tower_type = None
                                elif self.dragging_unit is None:  # Only start drag if not already dragging
                                    # Check if clicking on a unit
                                    clicked_on_unit = False
                                    for tower in self.towers:
                                        if tower.grid_x == grid_x and tower.grid_y == grid_y:
                                            # Deselect previous unit if any
                                            if self.selected_unit:
                                                self.selected_unit.is_selected = False
                                            tower.is_selected = True
                                            self.selected_unit = tower
                                            tower.start_drag(x, y)
                                            self.dragging_unit = tower
                                            clicked_on_unit = True
                                            break
                                    
                                    if not clicked_on_unit:
                                        for soldier in self.soldiers:
                                            if soldier.grid_x == grid_x and soldier.grid_y == grid_y:
                                                # Deselect previous unit if any
                                                if self.selected_unit:
                                                    self.selected_unit.is_selected = False
                                                soldier.is_selected = True
                                                self.selected_unit = soldier
                                                soldier.start_drag(x, y)
                                                self.dragging_unit = soldier
                                                clicked_on_unit = True
                                                break
                                    
                                    if not clicked_on_unit:
                                        # Deselect current unit if clicking on empty space
                                        if self.selected_unit:
                                            self.selected_unit.is_selected = False
                                            self.selected_unit = None
                    
                    elif event.button == 3:  # Right click
                        if self.selected_unit and isinstance(self.selected_unit, Soldier):
                            self.handle_soldier_rotation(mouse_pos)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.dragging_unit:  # Left click release
                        x, y = pygame.mouse.get_pos()
                        if x < SCREEN_WIDTH - 200:  # Only allow placement in the game area
                            grid_x = x // GRID_SIZE
                            grid_y = y // GRID_SIZE
                            
                            # Check if the new position is valid
                            if self.is_valid_tower_position(grid_x, grid_y):
                                self.dragging_unit.end_drag(grid_x, grid_y)
                            else:
                                # Return to original position if invalid
                                self.dragging_unit.end_drag(self.dragging_unit.grid_x, self.dragging_unit.grid_y)
                        
                        # Deselect the unit after moving
                        if self.selected_unit:
                            self.selected_unit.is_selected = False
                            self.selected_unit = None
                        self.dragging_unit = None
                
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging_unit:
                        x, y = pygame.mouse.get_pos()
                        self.dragging_unit.update_drag(x, y)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Deselect current unit
                        if self.selected_unit:
                            self.selected_unit.is_selected = False
                            self.selected_unit = None
                        # Also clear tower placement selection
                        self.selected_tower_type = None
                        self.dragging_unit = None
            
            # Update game state if not game over
            if not self.game_over:
                self.update()
            
            # Draw everything
            restart_button = self.draw()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit() 
