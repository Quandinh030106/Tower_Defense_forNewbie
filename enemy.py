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
        self.damage = 5  # Reduced base damage for all enemies (was 10)
        self.attack_cooldown = 0  # Add attack cooldown
        self.attack_rate = 30  # Attack every 30 frames (0.5 seconds at 60 FPS)
        self.angle = 0

    def move(self):
        if not self.path_index < len(self.path) - 1:
            self.reached_end = True
            return
            
        # Get current and next position
        current_x, current_y = self.path[self.path_index]
        next_x, next_y = self.path[self.path_index + 1]
        
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Check if there's a soldier blocking the next position
        for soldier in self.game.soldiers:
            if soldier.grid_x == next_x and soldier.grid_y == next_y:
                # Attack the soldier only if cooldown is ready
                if self.attack_cooldown <= 0:
                    soldier.take_damage(self.damage)
                    self.attack_cooldown = self.attack_rate
                return
        
        # Move towards next position if not attacking
        target_x = next_x * GRID_SIZE + GRID_SIZE // 2
        target_y = next_y * GRID_SIZE + GRID_SIZE // 2
        
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        self.angle = math.degrees(math.atan2(dy, dx))
        
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

        self.frames = load_enemy_row_frames("assets/enemy/Magma Crab.png", 64, 64, row=4, num_cols=8,scale_width = 64)

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 5
    
    def draw(self, screen: pygame.Surface):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        frame = self.frames[self.current_frame]
        angle_offset = -90
        rotated = pygame.transform.rotate(frame, -self.angle + angle_offset )
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect)

        # Draw health bar
        health_bar_length = 30
        health_ratio = self.health / self.max_health
        health_bar_width = max(0, health_ratio * health_bar_length)
        
        pygame.draw.rect(screen, RED, (int(self.x) - health_bar_length//2, int(self.y) - 25, health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (int(self.x) - health_bar_length//2, int(self.y) - 25, int(health_bar_width), 5))


class FastEnemy(Enemy):
    def __init__(self, path: List[Tuple[int, int]], game=None):
        super().__init__(path, speed=2.0, health=30, reward=7, game=game)
        self.damage = 3  # Fast enemy does less damage but attacks quickly
        self.attack_rate = 20  # Attacks more frequently

        self.frames = load_enemy_row_frames("assets/enemy/Leafbug.png", 64, 64, row=4, num_cols=8,scale_width = 64)

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 5
    
    def draw(self, screen: pygame.Surface):

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        frame = self.frames[self.current_frame]
        angle_offset = -90
        rotated = pygame.transform.rotate(frame, -self.angle + angle_offset)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect)
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
        self.damage = 12  # Tank does more damage but is slower
        self.attack_rate = 45  # Attacks more slowly

        self.frames = load_enemy_row_frames("assets/enemy/Firebug.png", 128, 64, row=4, num_cols=8,scale_width = 128)

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 5
    
    def draw(self, screen: pygame.Surface):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        frame = self.frames[self.current_frame]
        angle_offset = -90
        rotated = pygame.transform.rotate(frame, -self.angle + angle_offset)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect)
        # Draw health bar
        health_bar_length = 40
        health_ratio = self.health / self.max_health
        health_bar_width = max(0, health_ratio * health_bar_length)
        
        pygame.draw.rect(screen, RED, (int(self.x) - health_bar_length//2, int(self.y) - 30, health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (int(self.x) - health_bar_length//2, int(self.y) - 30, int(health_bar_width), 5)) 

class Boss(Enemy):
    def __init__(self, path: List[Tuple[int, int]], game=None):
        super().__init__(path, speed=1.25, health=400, reward=30, game=game)
        self.radius = 25
        self.damage = 20  # Boss does high damage
        self.attack_rate = 45

        self.frames = load_enemy_row_frames("assets/enemy/Scorpion.png", 64, 64, row=4, num_cols=8,scale_width = 64)

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 5
    
    def draw(self, screen: pygame.Surface):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        frame = self.frames[self.current_frame]
        angle_offset = -90
        rotated = pygame.transform.rotate(frame, -self.angle + angle_offset)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect)
        #Draw health bar
        health_bar_length = 60
        health_ratio = self.health / self.max_health
        health_bar_width = max(0, health_ratio * health_bar_length)

        pygame.draw.rect(screen, RED, (int(self.x) - health_bar_length//2, int(self.y) - 30, health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (int(self.x) - health_bar_length//2, int(self.y) - 30, int(health_bar_width), 5)) 
    
def load_enemy_row_frames(path: str, frame_width: int, frame_height: int, row: int, num_cols: int, scale_width: int = GRID_SIZE) -> List[pygame.Surface]:
    """
    Cắt một hàng cụ thể từ sprite sheet thành danh sách frame.

    :param path: đường dẫn đến file ảnh
    :param frame_width: chiều rộng mỗi frame
    :param frame_height: chiều cao mỗi frame
    :param row: hàng muốn cắt (tính từ 0)
    :param num_cols: số lượng cột trong hàng đó
    :return: list các frame đã cắt
    """
    sheet = pygame.image.load(path).convert_alpha()
    frames = []
    scale_height = int(scale_width * frame_height / frame_width)  # duy trì tỉ lệ gốc
    for col in range(num_cols):
        x = col * frame_width
        y = row * frame_height
        frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (scale_width, scale_height))
        frames.append(frame)
    return frames