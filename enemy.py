import math
import pygame
from typing import List, Tuple
from constants import *

class Enemy:
    def __init__(self, path: List[Tuple[int, int]], speed: float, health: int, reward: int, game=None):
        self.path = path
        self.path_index = 0
        grid_x, grid_y = path[0]
        self.x = grid_x * GRID_SIZE + GRID_SIZE // 2
        self.y = grid_y * GRID_SIZE + GRID_SIZE // 2
        self.speed = speed
        self.max_health = health
        self.health = health
        self.reward = reward
        self.radius = 15
        self.reached_end = False
        self.game = game
        self.damage = 10  # Base damage for all enemies
    
    def move(self):
        if not self.path_index < len(self.path) - 1:
            self.reached_end = True
            return
            
        # Get current and next position
        current_x, current_y = self.path[self.path_index]
        next_x, next_y = self.path[self.path_index + 1]
        
        # Check if there's a soldier blocking the next position
        for soldier in self.game.soldiers:
            if soldier.grid_x == next_x and soldier.grid_y == next_y:
                # Attack the soldier
                soldier.take_damage(self.damage)
                return
        
        # Move towards next position
        target_x = next_x * GRID_SIZE + GRID_SIZE // 2
        target_y = next_y * GRID_SIZE + GRID_SIZE // 2
        
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance < self.speed:
            self.path_index += 1
            self.x = target_x
            self.y = target_y
        else:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def take_damage(self, damage: int):
        self.health -= damage
    
    def is_dead(self) -> bool:
        return self.health <= 0
    
    def draw(self, screen: pygame.Surface):
        # Draw enemy
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        
        # Draw health bar
        health_bar_length = 30
        health_ratio = self.health / self.max_health
        health_bar_width = max(0, health_ratio * health_bar_length)
        
        pygame.draw.rect(screen, RED, (int(self.x) - health_bar_length//2, int(self.y) - 25, health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (int(self.x) - health_bar_length//2, int(self.y) - 25, int(health_bar_width), 5))


class BasicEnemy(Enemy):
    def __init__(self, path: List[Tuple[int, int]], game=None):
        super().__init__(path, speed=1.0, health=50, reward=5, game=game)
        self.damage = 10
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        # Draw eyes
        pygame.draw.circle(screen, BLACK, (int(self.x) - 5, int(self.y) - 5), 3)
        pygame.draw.circle(screen, BLACK, (int(self.x) + 5, int(self.y) - 5), 3)
        # Draw health bar
        health_bar_length = 30
        health_ratio = self.health / self.max_health
        health_bar_width = max(0, health_ratio * health_bar_length)
        
        pygame.draw.rect(screen, RED, (int(self.x) - health_bar_length//2, int(self.y) - 25, health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (int(self.x) - health_bar_length//2, int(self.y) - 25, int(health_bar_width), 5))


class FastEnemy(Enemy):
    def __init__(self, path: List[Tuple[int, int]], game=None):
        super().__init__(path, speed=2.0, health=30, reward=7, game=game)
        self.damage = 5
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius)
        # Draw eyes
        pygame.draw.circle(screen, BLACK, (int(self.x) - 5, int(self.y) - 5), 3)
        pygame.draw.circle(screen, BLACK, (int(self.x) + 5, int(self.y) - 5), 3)
        # Draw health bar
        health_bar_length = 30
        health_ratio = self.health / self.max_health
        health_bar_width = max(0, health_ratio * health_bar_length)
        
        pygame.draw.rect(screen, RED, (int(self.x) - health_bar_length//2, int(self.y) - 25, health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (int(self.x) - health_bar_length//2, int(self.y) - 25, int(health_bar_width), 5))


class TankEnemy(Enemy):
    def __init__(self, path: List[Tuple[int, int]], game=None):
        super().__init__(path, speed=1.0, health=150, reward=10, game=game)
        self.radius = 20
        self.damage = 20
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, PURPLE, (int(self.x), int(self.y)), self.radius)
        # Draw eyes
        pygame.draw.circle(screen, BLACK, (int(self.x) - 7, int(self.y) - 7), 4)
        pygame.draw.circle(screen, BLACK, (int(self.x) + 7, int(self.y) - 7), 4)
        # Draw health bar
        health_bar_length = 40
        health_ratio = self.health / self.max_health
        health_bar_width = max(0, health_ratio * health_bar_length)
        
        pygame.draw.rect(screen, RED, (int(self.x) - health_bar_length//2, int(self.y) - 30, health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (int(self.x) - health_bar_length//2, int(self.y) - 30, int(health_bar_width), 5)) 

class Boss(Enemy):
    def __init__(self, path: List[Tuple[int, int]], game=None):
        super().__init__(path, speed=1.5, health=400, reward=30, game=game)
        self.radius = 20
        self.damage = 30
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, PINK, (int(self.x), int(self.y)), self.radius)
        #Draw eyes
        pygame.draw.circle(screen, BLACK, (int(self.x)-7, int(self.y)-7), 4)
        pygame.draw.circle(screen, BLACK, (int(self.x)+7, int(self.y)-7), 4)
        #Draw health bar
        health_bar_length = 60
        health_ratio = self.health / self.max_health
        health_bar_width = max(0, health_ratio * health_bar_length)

        pygame.draw.rect(screen, RED, (int(self.x) - health_bar_length//2, int(self.y) - 30, health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (int(self.x) - health_bar_length//2, int(self.y) - 30, int(health_bar_width), 5)) 
    
