import math
import pygame
from typing import List, Optional
from constants import *

class Soldier:
    def __init__(self, grid_x: int, grid_y: int):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = grid_x * GRID_SIZE + GRID_SIZE // 2
        self.y = grid_y * GRID_SIZE + GRID_SIZE // 2
        self.health = 50
        self.max_health = 50
        self.damage = 5
        self.range = 60
        self.cooldown = 0
        self.fire_rate = 30
        self.radius = 15
        self.angle = 0
        self.is_selected = False
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def can_attack(self) -> bool:
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

    def attack(self, target: 'Enemy'):
        target.take_damage(self.damage)

    def is_dead(self) -> bool:
        return self.health <= 0

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

    def rotate(self, angle: float):
        self.angle = angle

    def draw(self, screen: pygame.Surface):
        # Draw selection indicator
        if self.is_selected:
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius + 2, 2)
            # Draw range circle when selected
            pygame.draw.circle(screen, (255, 255, 255, 100), (int(self.x), int(self.y)), self.range, 1)
        
        # Draw soldier body
        if self.is_dragging:
            # Draw semi-transparent soldier while dragging
            s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (0, 255, 0, 128), (self.radius, self.radius), self.radius)
            screen.blit(s, (self.x - self.radius, self.y - self.radius))
        else:
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.radius)
        
        # Draw soldier details with rotation
        if not self.is_dragging:
            # Calculate rotated points for the body
            body_length = 20
            body_width = 10
            angle_rad = math.radians(self.angle)
            
            # Draw rotated body
            body_points = [
                (self.x + body_width * math.cos(angle_rad), self.y + body_width * math.sin(angle_rad)),
                (self.x - body_width * math.cos(angle_rad), self.y - body_width * math.sin(angle_rad)),
                (self.x + body_length * math.cos(angle_rad), self.y + body_length * math.sin(angle_rad)),
                (self.x - body_length * math.cos(angle_rad), self.y - body_length * math.sin(angle_rad))
            ]
            pygame.draw.polygon(screen, BLUE, body_points)
            
            # Draw head
            head_x = self.x + (self.radius - 5) * math.cos(angle_rad)
            head_y = self.y + (self.radius - 5) * math.sin(angle_rad)
            pygame.draw.circle(screen, YELLOW, (int(head_x), int(head_y)), 5)
        
        # Draw health bar
        health_bar_length = 30
        health_ratio = self.health / self.max_health
        health_bar_width = max(0, health_ratio * health_bar_length)
        
        pygame.draw.rect(screen, RED, (int(self.x) - health_bar_length//2, int(self.y) - 25, health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (int(self.x) - health_bar_length//2, int(self.y) - 25, int(health_bar_width), 5)) 