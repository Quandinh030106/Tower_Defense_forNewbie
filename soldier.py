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
        self.health = 150
        self.max_health = 150
        self.damage = 8
        self.range = 60
        self.cooldown = 0
        self.fire_rate = 30
        self.radius = 15
        self.angle = 0
        self.is_selected = False
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.armor = 3
        self.regen_rate = 1
        self.regen_cooldown = 0
        self.regen_delay = 60


        self.image_original = pygame.image.load("assets/soldier/soldier.png").convert_alpha()


        scale_factor = GRID_SIZE / 96
        new_size = (int(96 * scale_factor), int(96 * scale_factor))
        self.image = pygame.transform.scale(self.image_original, new_size)

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def take_damage(self, damage: int):
        """Take damage from enemies. Updates the soldier's health and returns True if the soldier died."""
        actual_damage = max(1, damage - self.armor)
        self.health = max(0, self.health - actual_damage)
        self.regen_cooldown = self.regen_delay
        return self.health <= 0

    def can_attack(self) -> bool:
        return self.cooldown <= 0

    def reset_cooldown(self):
        self.cooldown = self.fire_rate

    def update_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            
        if self.regen_cooldown > 0:
            self.regen_cooldown -= 1
        elif self.health < self.max_health:
            self.health = min(self.max_health, self.health + self.regen_rate)

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
        # Vẽ vùng chọn và bán kính nếu đang chọn
        if self.is_selected:
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius + 2, 2)
            radius_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
            pygame.draw.circle(radius_surface, (255, 255, 255, 50), (self.range, self.range), self.range, width=1)
            screen.blit(radius_surface, (int(self.x) - self.range, int(self.y) - self.range))

        if self.is_dragging:
            # Vẽ vòng tròn bán trong suốt khi đang kéo
            s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (0, 255, 0, 128), (self.radius, self.radius), self.radius)
            screen.blit(s, (self.x - self.radius, self.y - self.radius))
        else:
            # Quay ảnh theo góc hiện tại
            rotated_image = pygame.transform.rotate(self.image, -self.angle)
            rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
            screen.blit(rotated_image, rotated_rect.topleft)

        # Vẽ thanh máu
        health_bar_length = 30
        health_ratio = self.health / self.max_health
        health_bar_width = max(0, health_ratio * health_bar_length)

        pygame.draw.rect(screen, RED, (int(self.x) - health_bar_length // 2, int(self.y) - 25, health_bar_length, 5))
        pygame.draw.rect(screen, GREEN,
                         (int(self.x) - health_bar_length // 2, int(self.y) - 25, int(health_bar_width), 5))

