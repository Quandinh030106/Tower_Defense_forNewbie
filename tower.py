import math
import pygame
from typing import List, Optional, Tuple
from constants import *
from projectile import Projectile

class Tower:
    def __init__(self, grid_x: int, grid_y: int, damage: int, range_radius: int, fire_rate: float, cost: int):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = grid_x * GRID_SIZE + GRID_SIZE // 2
        self.y = grid_y * GRID_SIZE + GRID_SIZE // 2
        self.damage = damage
        self.range = range_radius
        self.fire_rate = fire_rate
        self.cost = cost
        self.cooldown = 0
        self.is_selected = False
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
    
    def can_fire(self) -> bool:
        return self.cooldown <= 0

    def reset_cooldown(self):
        self.cooldown = self.fire_rate

    def update_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def find_target(self, enemies: List['Enemy']) -> Optional['Enemy']:
        # Find the closest enemy within range
        target = None
        min_distance = float('inf')
    
        for enemy in enemies:
            if enemy.health <= 0:
                continue
            
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and distance < min_distance:
                target = enemy
                min_distance = distance
    
        return target

    def fire(self, target: 'Enemy') -> Projectile:
        # Create a new projectile targeting the enemy
        return Projectile(self.x, self.y, target, self.damage, 5, YELLOW)

    def start_drag(self, mouse_x: int, mouse_y: int):
        self.is_dragging = True
        self.drag_offset_x = mouse_x - self.x
        self.drag_offset_y = mouse_y - self.y

    def update_drag(self, mouse_x: int, mouse_y: int):
        if self.is_dragging:
            self.x = mouse_x - self.drag_offset_x
            self.y = mouse_y - self.drag_offset_y

    def end_drag(self, grid_x: int, grid_y: int):
        self.is_dragging = False
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = grid_x * GRID_SIZE + GRID_SIZE // 2
        self.y = grid_y * GRID_SIZE + GRID_SIZE // 2

    def draw(self, screen: pygame.Surface, show_range: bool = False):
        # Draw selection indicator
        if self.is_selected:
            pygame.draw.rect(screen, YELLOW, 
                           (self.grid_x * GRID_SIZE - 2, self.grid_y * GRID_SIZE - 2, 
                            GRID_SIZE + 4, GRID_SIZE + 4), 2)
        
        # Draw range circle if selected
        if show_range or self.is_selected:
            pygame.draw.circle(screen, (255, 255, 255, 100), (int(self.x), int(self.y)), self.range, 1)
        
        # Draw tower body
        if self.is_dragging:
            # Draw semi-transparent tower while dragging
            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            s.fill((128, 128, 128, 128))
            screen.blit(s, (self.x - GRID_SIZE//2, self.y - GRID_SIZE//2))
        else:
            pygame.draw.rect(screen, GRAY, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)


class BasicTower(Tower):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(grid_x, grid_y, damage=10, range_radius=120, fire_rate=30, cost=50)
    
    def draw(self, screen: pygame.Surface, show_range: bool = False):
        # Draw range circle if selected
        if show_range or self.is_selected:
            pygame.draw.circle(screen, (255, 255, 255, 100), (int(self.x), int(self.y)), self.range, 1)
        
        # Draw tower body
        if self.is_dragging:
            # Draw semi-transparent tower while dragging
            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            s.fill((128, 128, 128, 128))
            screen.blit(s, (self.x - GRID_SIZE//2, self.y - GRID_SIZE//2))
        else:
            pygame.draw.rect(screen, GRAY, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            
            # Draw tower cannon
            pygame.draw.rect(screen, BLUE, (self.x - 5, self.y - 15, 10, 30))
            
            # Draw tower base outline
            pygame.draw.rect(screen, BLACK, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)


class RapidTower(Tower):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(grid_x, grid_y, damage=10, range_radius=120, fire_rate=15, cost=75)
    
    def draw(self, screen: pygame.Surface, show_range: bool = False):
        # Draw range circle if selected
        if show_range or self.is_selected:
            pygame.draw.circle(screen, (255, 255, 255, 100), (int(self.x), int(self.y)), self.range, 1)
        
        # Draw tower body
        if self.is_dragging:
            # Draw semi-transparent tower while dragging
            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            s.fill((128, 128, 128, 128))
            screen.blit(s, (self.x - GRID_SIZE//2, self.y - GRID_SIZE//2))
        else:
            pygame.draw.rect(screen, GRAY, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            
            # Draw tower cannon
            pygame.draw.rect(screen, BLUE, (self.x - 5, self.y - 15, 10, 30))
            
            # Draw tower base outline
            pygame.draw.rect(screen, BLACK, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)


class SniperTower(Tower):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(grid_x, grid_y, damage=30, range_radius=200, fire_rate=60, cost=100)
    
    def draw(self, screen: pygame.Surface, show_range: bool = False):
        if show_range or self.is_selected:
            pygame.draw.circle(screen, (255, 255, 255, 100), (int(self.x), int(self.y)), self.range, 1)
        
        # Draw tower body
        if self.is_dragging:
            # Draw semi-transparent tower while dragging
            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            s.fill((128, 128, 128, 128))
            screen.blit(s, (self.x - GRID_SIZE//2, self.y - GRID_SIZE//2))
        else:
            pygame.draw.rect(screen, GRAY, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            
            # Draw tower cannon (sniper)
            pygame.draw.rect(screen, RED, (self.x - 3, self.y - 20, 6, 40))
            
            # Draw tower base outline
            pygame.draw.rect(screen, BLACK, (self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2) 
