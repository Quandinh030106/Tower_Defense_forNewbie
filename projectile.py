import math
import pygame

class Projectile:
    def __init__(self, x: int, y: int, target, damage: int, speed: int, color: tuple):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = speed
        self.color = color
        self.radius = 5
        self.hit = False

    def move(self) -> bool:
        if self.target.health <= 0:
            return True  # Target is dead, remove projectile
        
        # Calculate direction to target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Check if we hit the target
        if distance < self.radius + self.target.radius:
            self.target.take_damage(self.damage)
            return True  # Hit, remove projectile
        
        # Normalize and move
        if distance > 0:
            dx /= distance
            dy /= distance
            self.x += dx * self.speed
            self.y += dy * self.speed
        
        return False  # Keep moving
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius) 