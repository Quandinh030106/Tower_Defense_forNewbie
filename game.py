import pygame
import sys
import math
import random
from typing import List, Tuple, Dict, Optional

from constants import *
from tower import Tower, BasicTower, RapidTower, SniperTower
from soldier import Soldier
from enemy import Enemy, BasicEnemy, FastEnemy, TankEnemy, Boss
from projectile import Projectile
from menu import Menu
from maps import get_map_path, get_map_description, get_difficulty_settings

class Game:
    def __init__(self, map_name: str = "Forest", difficulty: str = "Medium"):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense 8-bit")
        self.clock = pygame.time.Clock()
        
        self.map_name = map_name
        self.difficulty = difficulty
        self.reset_game()
        self.current_path = get_map_path(self.map_name)
        self.background_image = self.load_map_image(self.map_name)  # Thêm dòng này

    def load_map_image(self, map_name: str) -> Optional[pygame.Surface]:
        image_path = f"assets/map/{map_name.lower().replace(' ', '_')}.png"  # Giả sử bạn lưu ảnh trong thư mục assets/maps và định dạng là .png
        try:
            image = pygame.image.load(image_path).convert_alpha()
            # Kéo dài hình ảnh để vừa với khu vực trò chơi (SCREEN_WIDTH - 200, SCREEN_HEIGHT)
            return pygame.transform.scale(image, (SCREEN_WIDTH - 200, SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Không thể tải hình ảnh bản đồ {image_path}: {e}")
            return None
    def reset_game(self):
        # Get difficulty settings
        settings = get_difficulty_settings(self.difficulty)
        
        self.gold = settings["starting_gold"]
        self.lives = settings["starting_lives"]
        self.wave = 1
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
        self.dragging_enabled = False
        # Get map path
        self.current_path = get_map_path(self.map_name)

        self.killed_enemies = 0

    def is_valid_tower_position(self, grid_x: int, grid_y: int) -> bool:
        # Check if position is on a path
        if (grid_x, grid_y) in self.current_path:
            return False
        
        # Check if position is already occupied by a tower
        for tower in self.towers:
            if tower.grid_x == grid_x and tower.grid_y == grid_y:
                return False
        
        # Check if position is within game boundaries
        if grid_x < 0 or grid_x >= SCREEN_WIDTH // GRID_SIZE - 5 or grid_y < 0 or grid_y >= SCREEN_HEIGHT // GRID_SIZE:
            return False
            
        return True

    def is_valid_soldier_position(self, grid_x: int, grid_y: int) -> bool:
        # Check if position is on a path
        if (grid_x, grid_y) not in self.current_path:
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
        # For soldiers, we need to check soldier position validity first
        if self.selected_tower_type == "soldier" and self.gold >= 75:
            if self.is_valid_soldier_position(grid_x, grid_y):
                self.soldiers.append(Soldier(grid_x, grid_y))
                self.gold -= 75
                return True
            return False
            
        # For towers, check tower position validity
        if not self.is_valid_tower_position(grid_x, grid_y):
            return False
            
        if self.selected_tower_type == "basic_tower" and self.gold >= 50:
            self.towers.append(BasicTower(grid_x, grid_y))
            self.gold -= 50
            return True
        elif self.selected_tower_type == "sniper_tower" and self.gold >= 100:
            tower = SniperTower(grid_x, grid_y)
            tower.game = self
            self.towers.append(tower)
            self.gold -= 100
            return True

        elif self.selected_tower_type == "rapid_tower" and self.gold >= 75:
            self.towers.append(RapidTower(grid_x, grid_y))
            self.gold -= 75
            return True
            
        return False
    
    def start_wave(self):
        if not self.wave_in_progress:
            self.wave_in_progress = True
            self.spawn_enemies()
    
    def spawn_enemies(self):
        settings = get_difficulty_settings(self.difficulty)
        # Base number of enemies increases by 50% each wave
        base_num_enemies = int(5 * (1.5 ** (self.wave - 1)))
        num_enemies = int(base_num_enemies * settings["wave_size_multiplier"])
        
        # Different mix of enemies based on wave number
        num_basic = max(3, num_enemies - self.wave * 2)
        num_fast = min(self.wave, num_enemies // 3)
        num_tank = max(0, min(self.wave // 3, 3))
        num_boss = self.wave // 10
        
        # Spawn delay between enemies (decreases by 10% each wave, minimum 10)
        self.spawn_delay = max(10, int(30 * (0.9 ** (self.wave - 1))))
        self.spawn_counter = 0
        
        # Prepare enemy queue
        self.enemy_queue = []
        for _ in range(num_basic):
            self.enemy_queue.append("basic")
        for _ in range(num_fast):
            self.enemy_queue.append("fast")
        for _ in range(num_tank):
            self.enemy_queue.append("tank")
        for _ in range(num_boss):
            self.enemy_queue.append('boss')
        # Shuffle queue for variety
        random.shuffle(self.enemy_queue)
    
    def spawn_enemy_from_queue(self):
        if not self.enemy_queue:
            return
            
        settings = get_difficulty_settings(self.difficulty)
        enemy_type = self.enemy_queue.pop(0)
        
        if enemy_type == "basic":
            enemy = BasicEnemy(self.current_path, self)
        elif enemy_type == "fast":
            enemy = FastEnemy(self.current_path, self)
        elif enemy_type == "tank":
            enemy = TankEnemy(self.current_path, self)
        elif enemy_type == 'boss':
            enemy = Boss(self.current_path, self)
        
        # Apply difficulty multipliers and wave scaling (7% increase per wave)
        wave_multiplier = 1.0 + (0.07 * (self.wave - 1))  # 7% increase per wave
        
        enemy.health = int(enemy.health * settings["enemy_health_multiplier"] * wave_multiplier)
        enemy.max_health = enemy.health
        enemy.speed *= settings["enemy_speed_multiplier"] * wave_multiplier
        enemy.reward = int(enemy.reward * settings["enemy_reward_multiplier"] * wave_multiplier)
        enemy.damage = int(enemy.damage * settings["enemy_health_multiplier"] * wave_multiplier)
        
        self.enemies.append(enemy)
    
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
            self.gold += 30 + (self.wave * 2)  # Gold reward for completing wave
        
        # Update towers
        for tower in self.towers:
            tower.update_cooldown(self.enemies)
            if tower.can_fire():
                target = tower.find_target(self.enemies)
                if target:
                    result = tower.fire(target)
                    if isinstance(result, list):
                        self.projectiles.extend(result)
                    else:
                        self.projectiles.append(result)

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
                self.killed_enemies += 1
                self.enemies.remove(enemy)
    
    def draw_grid(self):
        # Set grid color based on map theme
        if self.map_name == "Forest":
            grid_color = (0, 100, 0)  # Dark forest green
        elif self.map_name == "Flame Desert":
            grid_color = (184, 134, 11)  # Dark goldenrod
        elif self.map_name == "Ice Kingdom":
            grid_color = (220, 220, 220)  # Light gray
        else:
            grid_color = (50, 50, 50)

        # Draw grid lines
        for x in range(0, SCREEN_WIDTH - 200, GRID_SIZE):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, grid_color, (0, y), (SCREEN_WIDTH - 200, y))
    
    def draw_path(self):
        """
        # Set path color based on map theme
        if self.map_name == "Forest":
            path_color = (139, 69, 19)  # Brown dirt path
        elif self.map_name == "Flame Desert":
            path_color = (160, 82, 45)  # Sandy path
        elif self.map_name == "Ice Kingdom":
            path_color = (169, 169, 169)  # Gray snow path
        else:
            path_color = BROWN
            
        for grid_x, grid_y in self.current_path:
            pygame.draw.rect(self.screen, path_color, (grid_x * GRID_SIZE, grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        """
        pass

    def draw_map_info(self):
        #draw game info
        gold_text = GAME_FONT.render(f"Gold: {self.gold}", True, WHITE)
        wave_text = GAME_FONT.render(f"Wave: {self.wave}", True, WHITE)
        lives_text = GAME_FONT.render(f"Lives: {self.lives}", True, WHITE)
        killed_text = GAME_FONT.render(f"Killed: {self.killed_enemies}", True, WHITE)

        self.screen.blit(gold_text, (SCREEN_WIDTH - 190, 10))
        self.screen.blit(wave_text, (SCREEN_WIDTH - 190, 35))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 190, 60))
        self.screen.blit(killed_text, (SCREEN_WIDTH - 190, 85))

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
        # Draw background with map-specific theme
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            # Nếu không có hình ảnh, vẫn tô màu nền như cũ
            if self.map_name == "Forest":
                self.screen.fill((34, 139, 34))
            elif self.map_name == "Flame Desert":
                self.screen.fill((210, 180, 140))
            elif self.map_name == "Ice Kingdom":
                self.screen.fill((240, 248, 255))
            else:
                self.screen.fill(DARK_GREEN)
        
        # Draw grid
        self.draw_grid()
        
        # Draw path
        self.draw_path()
        
        # Draw tower ranges
        for tower in self.towers:
            if tower == self.selected_tower:
                center_x = tower.grid_x * GRID_SIZE + GRID_SIZE // 2
                center_y = tower.grid_y * GRID_SIZE + GRID_SIZE // 2
                radius = tower.range


                pygame.draw.circle(self.screen, (255, 255, 255), (center_x, center_y), radius, width=1)

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
        self.menu.selected_tower = self.selected_tower
        self.menu.draw(self.screen, self.gold, self.wave, self.lives, self.dragging_enabled, can_sell=bool(self.selected_tower))

        self.draw_map_info()
        
        # Draw game over screen
        restart_button = None
        if self.game_over:
            restart_button = self.draw_game_over()

        # Draw tower preview (when placing a new tower)
        if self.selected_tower_type:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < SCREEN_WIDTH - 200:
                grid_x = mouse_x // GRID_SIZE
                grid_y = mouse_y // GRID_SIZE
                center_x = grid_x * GRID_SIZE + GRID_SIZE // 2
                center_y = grid_y * GRID_SIZE + GRID_SIZE // 2

                # Draw preview based on type
                if self.selected_tower_type == "soldier":
                    # For soldier, show range and a semi-transparent soldier preview
                    if self.is_valid_soldier_position(grid_x, grid_y):
                        # Draw range circle
                        range_radius = 60
                        radius_surface = pygame.Surface((range_radius * 2, range_radius * 2), pygame.SRCALPHA)
                        pygame.draw.circle(radius_surface, (255, 255, 255, 50), (range_radius, range_radius), range_radius, width=1)
                        self.screen.blit(radius_surface, (center_x - range_radius, center_y - range_radius))

                        # Draw semi-transparent soldier preview
                        s = pygame.Surface((30, 30), pygame.SRCALPHA)  # 30 is soldier diameter
                        pygame.draw.circle(s, (0, 255, 0, 128), (15, 15), 15)  # Green semi-transparent circle
                        self.screen.blit(s, (center_x - 15, center_y - 15))
                else:
                    # Determine tower range (based on type)
                    if self.selected_tower_type == "basic_tower":
                        range_radius = 120
                        color = GRAY
                    elif self.selected_tower_type == "sniper_tower":
                        range_radius = 200
                        color = GRAY
                    elif self.selected_tower_type == "rapid_tower":
                        range_radius = 120
                        color = GRAY
                    else:
                        range_radius = 0
                        color = (0, 0, 0)

                    # Draw semi-transparent tower
                    s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                    s.fill((*color, 100))  # semi-transparent
                    self.screen.blit(s, (grid_x * GRID_SIZE, grid_y * GRID_SIZE))

                    # Draw radius
                    radius_surface = pygame.Surface((range_radius * 2, range_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(radius_surface, (255, 255, 255, 50), (range_radius, range_radius), range_radius)
                    self.screen.blit(radius_surface, (center_x - range_radius, center_y - range_radius))

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
